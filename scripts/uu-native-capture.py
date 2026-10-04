#!/usr/bin/python3
"""Own one ScreenCast session and pass its authorized PipeWire FD to a worker."""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import uuid

from gi.repository import Gio, GLib

PORTAL = 'org.freedesktop.portal.Desktop'
OBJECT = '/org/freedesktop/portal/desktop'
CAST = 'org.freedesktop.portal.ScreenCast'


class Session:
    def __init__(self):
        self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.path = None

    def request(self, method, signature, args, options):
        token = 'plus_' + uuid.uuid4().hex
        options = {**options, 'handle_token': GLib.Variant('s', token)}
        request = OBJECT + '/request/' + self.bus.get_unique_name()[1:].replace('.', '_') + '/' + token
        loop = GLib.MainLoop()
        answer = []
        def response(_bus, _sender, _path, _interface, _signal, parameters, _data):
            answer.extend(parameters.unpack())
            loop.quit()
        subscription = self.bus.signal_subscribe(PORTAL, 'org.freedesktop.portal.Request',
            'Response', request, None, Gio.DBusSignalFlags.NONE, response, None)
        timer = GLib.timeout_add_seconds(120, lambda: loop.quit() or False)
        try:
            self.bus.call_sync(PORTAL, OBJECT, CAST, method,
                GLib.Variant(signature, (*args, options)), GLib.VariantType.new('(o)'),
                Gio.DBusCallFlags.NONE, 10000, None)
            loop.run()
            if not answer or answer[0]:
                raise RuntimeError(f'{method}: consent cancelled, denied or timed out')
            return answer[1]
        finally:
            self.bus.signal_unsubscribe(subscription)
            if GLib.MainContext.default().find_source_by_id(timer):
                GLib.source_remove(timer)

    def start(self, restore_file):
        result = self.request('CreateSession', '(a{sv})', (),
            {'session_handle_token': GLib.Variant('s', 'plus_' + uuid.uuid4().hex)})
        self.path = result['session_handle']
        options = {'types': GLib.Variant('u', 1), 'multiple': GLib.Variant('b', False),
                   'cursor_mode': GLib.Variant('u', 2), 'persist_mode': GLib.Variant('u', 2)}
        if restore_file.is_file():
            options['restore_token'] = GLib.Variant('s', restore_file.read_text().strip())
        self.request('SelectSources', '(oa{sv})', (self.path,), options)
        result = self.request('Start', '(osa{sv})', (self.path, ''), {})
        if 'restore_token' in result:
            restore_file.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            restore_file.write_text(result['restore_token'] + '\n')
            restore_file.chmod(0o600)
        streams = result['streams']
        if len(streams) != 1:
            raise RuntimeError('Expected one selected monitor')
        node, info = streams[0]
        result, descriptors = self.bus.call_with_unix_fd_list_sync(PORTAL, OBJECT, CAST,
            'OpenPipeWireRemote', GLib.Variant('(oa{sv})', (self.path, {})),
            GLib.VariantType.new('(h)'), Gio.DBusCallFlags.NONE, 10000, None, None)
        return descriptors.get(result.unpack()[0]), node, info

    def close(self):
        if self.path:
            self.bus.call_sync(PORTAL, self.path, 'org.freedesktop.portal.Session', 'Close',
                None, None, Gio.DBusCallFlags.NONE, 5000, None)
            self.path = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend', choices=['cpu', 'gpu'], required=True)
    parser.add_argument('--worker', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--duration', type=int, default=0)
    parser.add_argument('--gpu-socket-fd', type=int)
    parser.add_argument('--gpu-socket', type=Path)
    args = parser.parse_args()
    os.umask(0o077)
    args.runtime.mkdir(parents=True, exist_ok=True)
    session = Session()
    process = None
    descriptor = None
    listener = peer = None
    try:
        descriptor, node, info = session.start(args.runtime / 'portal-restore-token')
        inherited = [descriptor]
        environment = {**os.environ}
        if args.backend == 'cpu':
            environment.update(UUR_PW_FD=str(descriptor), UUR_PW_NODE=str(node),
                               UUR_FRAME_PATH=str(args.runtime / 'frames.v1'))
            if info.get('pipewire-serial'):
                environment['UURB_CAPTURE_TARGET_SERIAL'] = str(info['pipewire-serial'])
            command = [str(args.worker)]
        else:
            if args.gpu_socket_fd is None:
                if args.gpu_socket is None:
                    raise RuntimeError('GPU requires the capture consumer socket FD or endpoint')
                listener = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
                listener.bind(str(args.gpu_socket))
                listener.listen(1)
                listener.settimeout(120)
                (args.runtime / 'portal-ready.json').write_text(json.dumps(
                    {'backend': args.backend, 'node': node, 'properties': info,
                     'endpoint': str(args.gpu_socket), 'waiting_for_consumer': True}) + '\n')
                peer, _ = listener.accept()
                args.gpu_socket_fd = peer.fileno()
            inherited.append(args.gpu_socket_fd)
            environment.update(UURB_CAPTURE_SIZE='3840x2160', UURB_CAPTURE_MAX_FPS='60')
            if info.get('pipewire-serial'):
                environment['UURB_CAPTURE_TARGET_SERIAL'] = str(info['pipewire-serial'])
            command = [str(args.worker), str(descriptor), str(node), '--gpu-relay',
                       str(args.gpu_socket_fd)]
        (args.runtime / 'portal-ready.json').write_text(json.dumps(
            {'backend': args.backend, 'node': node, 'properties': info}) + '\n')
        process = subprocess.Popen(command, env=environment, pass_fds=inherited)
        def stop(*_):
            if process.poll() is None:
                process.terminate()
        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        try:
            result = process.wait(timeout=args.duration or None)
        except subprocess.TimeoutExpired:
            process.terminate()
            result = process.wait(timeout=5)
        if result not in (0, -signal.SIGTERM):
            raise RuntimeError(f'Capture worker exited with {result}')
    finally:
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        if descriptor is not None:
            os.close(descriptor)
        if peer:
            peer.close()
        if listener:
            listener.close()
            args.gpu_socket.unlink(missing_ok=True)
        session.close()


if __name__ == '__main__':
    main()
