#!/usr/bin/env python3
"""Run the selected SteamOS relay and Proton workers in a portable sandbox."""
import json
import fcntl
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import time

root = Path(os.environ['UURB_STEAMOS_ROOT'])
prefix = Path(os.environ['WINEPREFIX'])
proton = os.environ['UURB_PROTON']
app = prefix / 'drive_c/Program Files/Netease/GameViewer'
compat = root / 'build/compat'
private_display = ':' + os.environ.get('UURB_PRIVATE_DISPLAY', '20')
rdp_port = int(os.environ.get('UURB_RDP_PORT', '3399'))
monitor = os.environ.get('UURB_MONITOR', '0')
workers = []
running = True
instance_lock = None
owns_prefix = False
physical_env = dict(os.environ)
manager_env = dict(os.environ)
manager_host = None
env = dict(os.environ)


def log(message):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), message, flush=True)


def spawn(name, command, selected_env=None):
    output = (root / 'logs' / f'{name}.log').open('ab', buffering=0)
    process = subprocess.Popen(command, env=selected_env or env, stdout=output,
                               stderr=subprocess.STDOUT, cwd=app if app.exists() else root)
    output.close()
    workers.append((name, process))
    return process


def run(command, selected_env=None, timeout=30):
    return subprocess.run(command, env=selected_env or env, check=True, timeout=timeout,
                          cwd=app if app.exists() else root, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


def proton_command(*arguments):
    return [proton, 'runinprefix', *map(str, arguments)]


def wait_until(predicate, description, seconds=30):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline and running:
        if predicate():
            return
        for name, process in workers:
            if not name.startswith('manager') and process.poll() is not None:
                raise RuntimeError(f'{name} exited ({process.returncode}); see logs/{name}.log')
        time.sleep(0.2)
    raise RuntimeError(f'Timed out waiting for {description}')


def listening(port):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=0.2):
            return True
    except OSError:
        return False


def window_ids():
    result = subprocess.run(['xdotool', 'search', '--name', '^SteamOS-Desktop-Relay$'],
                            env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.decode().split()


def request_stop(*_):
    global running
    running = False


def send_reply(client, message):
    # A health probe may time out while a manager window is being opened.
    # Losing that client must never tear down the desktop relay.
    try:
        client.sendall(message)
        return True
    except (BrokenPipeError, ConnectionResetError):
        return False


def find_manager(visible=False):
    result = subprocess.run(['xdotool', 'search', *(['--onlyvisible'] if visible else []), '--name', '^(网易UU远程|UU Remote)$'],
                            env=manager_env, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    for window in result.stdout.decode().split():
        geometry = subprocess.run(['xdotool', 'getwindowgeometry', '--shell', window],
                   env=manager_env, stdout=subprocess.PIPE,
                   stderr=subprocess.DEVNULL).stdout.decode()
        dimensions = dict(line.split('=', 1) for line in geometry.splitlines() if '=' in line)
        if int(dimensions.get('WIDTH', '0')) >= 640 and int(dimensions.get('HEIGHT', '0')) >= 360:
            return window
    return None


def manager_running():
    for process in Path('/proc').iterdir():
        try:
            if process.stat().st_uid != os.getuid():
                continue
            values = dict(item.split('=', 1) for item in
                          process.joinpath('environ').read_text().split('\0') if '=' in item)
            if values.get('WINEPREFIX') and Path(values['WINEPREFIX']) == prefix:
                # UU changes argv[0]/comm to "source=explorer.exe". Its mapped
                # PE image identifies the real client, independent of that name.
                executable = str(app / 'bin/GameViewer.exe')
                if any(line.endswith(' ' + executable) for line in
                       process.joinpath('maps').read_text().splitlines()):
                    return True
        except (OSError, ValueError):
            continue
    return False


def manager_surface():
    if manager_host is None or manager_host.poll() is not None:
        return None
    # Xephyr does not publish _NET_WM_PID on its host window. Its unique
    # instance class identifies this installation's display instead.
    name = 'uurb-manager-' + manager_env['DISPLAY'].lstrip(':')
    result = subprocess.run(['xdotool', 'search', '--classname', '^' + name + '$'],
               env=physical_env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return next(iter(result.stdout.decode().split()), None)


def prepare_manager_display():
    global manager_host, manager_env
    if manager_host is not None and manager_host.poll() is None:
        return
    for binary in ('Xephyr', 'openbox', 'xcompmgr'):
        if not (root / 'tools/runtime/usr/bin' / binary).is_file():
            raise RuntimeError('Run setup to install the compact UU display runtime.')
    display = ':' + str(int(private_display[1:]) + 1)
    authority = root / 'runtime/manager.xauth'
    authority.touch(mode=0o600, exist_ok=True)
    run(['xauth', '-f', str(authority), 'add', display, '.', secrets.token_hex(16)])
    manager_env = {**physical_env, 'DISPLAY': display, 'XAUTHORITY': str(authority)}
    manager_env.pop('WAYLAND_DISPLAY', None)
    selected = {**physical_env, 'LD_LIBRARY_PATH': str(root / 'tools/runtime/usr/lib')}
    manager_host = spawn('manager-xephyr', [str(root / 'tools/runtime/usr/bin/Xephyr'),
        display, '-screen', os.environ.get('UURB_RESOLUTION', '1280x800'),
        '-title', 'UU Remote', '-name', 'uurb-manager-' + display[1:], '-no-host-grab', '-noreset',
        '-nolisten', 'tcp', '-nolisten', 'local', '-auth', str(authority)], selected)
    wait_until(lambda: subprocess.run(['xdotool', 'getdisplaygeometry'], env=manager_env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
        'UU window display')
    spawn('manager-openbox', [str(root / 'tools/runtime/usr/bin/openbox'), '--sm-disable',
        '--config-file', str(root / 'tools/runtime/etc/xdg/openbox/rc.xml')],
        {**manager_env, 'LD_LIBRARY_PATH': str(root / 'tools/runtime/usr/lib'),
         'XDG_DATA_DIRS': f'{root}/tools/runtime/usr/share:/usr/share'})
    spawn('manager-compositor', [str(root / 'tools/runtime/usr/bin/xcompmgr'), '-n'],
          {**manager_env, 'LD_LIBRARY_PATH': str(root / 'tools/runtime/usr/lib')})
    spawn('manager-menus', ['/usr/bin/python3', '-B',
          str(Path(__file__).with_name('uu-steamos-menus.py'))], manager_env)


def open_manager(context=None):
    context = context or {}
    gamescope = physical_env.get('UURB_SESSION_KIND') == 'gamescope'
    if gamescope:
        appid = str(context.get('appid', '0'))
        if appid.isdecimal() and 0 < int(appid) < 2**32:
            display = context.get('display', physical_env['DISPLAY'])
            if display in physical_env.get('UURB_HOST_DISPLAYS', physical_env['DISPLAY']).split(','):
                physical_env['DISPLAY'] = display
            physical_env['SteamAppId'] = appid
            physical_env['STEAM_COMPAT_APP_ID'] = appid
            physical_env['SteamGameId'] = str(context.get('gameid', appid))
        prepare_manager_display()
    # Always restore the actual client rather than mapping an empty Wine desktop.
    spawn('manager', proton_command('explorer', '/desktop=root',
          r'C:\Program Files\Netease\GameViewer\GameViewer.exe'), manager_env)
    wait_until(lambda: manager_running() and find_manager() is not None,
               'native UU management window', seconds=45)
    window = find_manager()
    if gamescope:
        surface = manager_surface()
        if not surface:
            raise RuntimeError('UU display surface is unavailable')
        appid = physical_env['SteamAppId']
        if appid != '0':
            run(['xprop', '-id', surface, '-f', 'STEAM_GAME', '32c',
                 '-set', 'STEAM_GAME', appid], physical_env)
        run(['xdotool', 'windowmap', surface, 'windowraise', surface], physical_env)
        # Nested focus needs the host surface to be presented first. Waiting
        # synchronously before Steam knows that surface would deadlock launch.
        run(['xdotool', 'windowmap', window, 'windowactivate', window], manager_env)
    else:
        run(['xdotool', 'windowmap', '--sync', window, 'windowactivate', '--sync', window], manager_env)


def manager_visible():
    visible = manager_running() and find_manager(visible=True) is not None
    if not visible and physical_env.get('UURB_SESSION_KIND') == 'gamescope':
        surface = manager_surface()
        if surface:
            # Steam should not retain a blank nested display after UU closes.
            run(['xdotool', 'windowunmap', surface], physical_env)
    return visible


def serve():
    global instance_lock, owns_prefix
    instance_lock = (root / 'runtime/instance.lock').open('a')
    try:
        fcntl.flock(instance_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise RuntimeError('Another portable session or setup owns this prefix.')
    owns_prefix = True
    record = {'pid': os.getpid(), 'start': Path('/proc/self/stat').read_text()
              .rsplit(')', 1)[1].split()[19]}
    (root / 'runtime/supervisor.json').write_text(json.dumps(record))
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    if not (app / 'GameViewer.exe').is_file():
        raise RuntimeError('UU is not installed; run uu-steamos setup first.')
    gamescope = env.get('UURB_SESSION_KIND') == 'gamescope'
    if not gamescope:
        password_file = root / 'config/rdp-password'
        if not password_file.exists():
            password_file.write_text(secrets.token_hex(24))
            password_file.chmod(0o600)
        password = password_file.read_text().strip()
        if listening(rdp_port):
            raise RuntimeError(f'Loopback port {rdp_port} is already occupied.')
        krdp_version = run(['pacman', '-Q', 'krdp'], physical_env).stdout.decode().strip()
        if not krdp_version.startswith('krdp 6.4.3-'):
            raise RuntimeError(f'KRDP input shim requires reviewed 6.4.3; found {krdp_version}')
        spawn('krdp', ['krdpserver', '--plasma', '--monitor', monitor, '--address', '127.0.0.1', '--port', str(rdp_port),
                      '--username', 'uurb', '--password', password,
                      '--certificate', str(root / 'tls/server.crt'),
                      '--certificate-key', str(root / 'tls/server.key')],
              {**env, 'QT_QPA_PLATFORM': 'wayland', 'LD_PRELOAD': str(compat / 'uu-krdp-input-auth.so'),
               'QT_LOGGING_RULES': 'org.kde.krdp.debug=false'})
        wait_until(lambda: listening(rdp_port), 'KRDP listener')
        log(f'KRDP is listening on 127.0.0.1:{rdp_port} using Plasma protocols.')
    resolution = os.environ.get('UURB_RESOLUTION', '1280x800')
    if resolution not in ('1280x800', '1280x720', '1920x1080', '2560x1440', '3840x2160'):
        raise RuntimeError('Unsupported UURB_RESOLUTION.')
    authority = root / 'runtime/private.xauth'
    authority.touch(mode=0o600, exist_ok=True)
    run(['xauth', '-f', str(authority), 'add', private_display, '.', secrets.token_hex(16)])
    env.update(DISPLAY=private_display, XAUTHORITY=str(authority), UURB_INPUT_ROUTE='legacy')
    env.pop('WAYLAND_DISPLAY', None)
    spawn('xvfb', [str(root / 'tools/runtime/usr/bin/Xvfb'), private_display, '-screen', '0',
                   f'{resolution}x24', '-dpi', '96', '-nolisten', 'tcp', '-nolisten',
                   'local', '-noreset', '-auth', str(authority)])
    wait_until(lambda: subprocess.run(['xdotool', 'getdisplaygeometry'], env=env,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
               'private X display')
    spawn('openbox', [str(root / 'tools/runtime/usr/bin/openbox'), '--sm-disable',
                     '--config-file', str(root / 'tools/runtime/etc/xdg/openbox/rc.xml')],
          {**env, 'LD_LIBRARY_PATH': str(root / 'tools/runtime/usr/lib'),
           'XDG_DATA_DIRS': f'{root}/tools/runtime/usr/share:/usr/share'})
    if gamescope:
        width, height = resolution.split('x')
        capture = spawn('gamescope-video', ['gst-launch-1.0', '-q',
            'pipewiresrc', 'target-object=gamescope', '!', 'video/x-raw,format=BGRx',
            '!', 'queue', 'max-size-buffers=2', 'leaky=downstream', '!',
            'videoscale', '!', f'video/x-raw,width={width},height={height}',
            '!', 'ximagesink', 'sync=false', 'force-aspect-ratio=false',
            'handle-events=false'])
        def capture_windows():
            result = subprocess.run(['xdotool', 'search', '--pid', str(capture.pid)],
                        env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            return result.stdout.decode().split()
        wait_until(lambda: bool(capture_windows()), 'gamescope video canvas')
        for window in capture_windows():
            run(['xdotool', 'set_window', '--name', 'SteamOS-Desktop-Relay', window,
                 'windowunmap', window])
            run(['xprop', '-id', window, '-f', '_NET_WM_STATE', '32a',
                 '-set', '_NET_WM_STATE', '_NET_WM_STATE_FULLSCREEN'])
            run(['xdotool', 'windowmap', window, 'windowmove', window, '0', '0',
                 'windowsize', window, width, height])
        input_ready = root / 'runtime/gamescope-input.ready'
        input_ready.unlink(missing_ok=True)
        spawn('gamescope-input', ['/usr/bin/python3', '-B',
              str(Path(__file__).with_name('uu-gamescope-input.py'))])
        wait_until(input_ready.exists, 'gamescope EIS input seat')
    else:
        # The native RDP viewer owns the canvas. XTEST forwards UU events to it.
        fingerprint = run(['openssl', 'x509', '-in', str(root / 'tls/server.crt'),
                           '-outform', 'DER']).stdout
        import hashlib
        arguments = [f'/v:127.0.0.1:{rdp_port}', '/u:uurb', f'/p:{password}',
                     f'/cert:fingerprint:sha256:{hashlib.sha256(fingerprint).hexdigest()}',
                     '/title:SteamOS-Desktop-Relay', f'/size:{resolution}', '/f',
                     '/gfx:AVC420', '/audio-mode:2', '-clipboard', '-decorations',
                     '-grab-keyboard', '/log-level:WARN']
        arguments_file = root / 'runtime/rdp-args'
        arguments_file.write_text('\n'.join(arguments) + '\n')
        arguments_file.chmod(0o600)
        spawn('rdp', ['xfreerdp3', f'/args-from:{arguments_file}'])
        wait_until(lambda: bool(window_ids()), 'RDP canvas', seconds=45)
    # Initialize Wine services on the private canvas, keeping the host display free.
    spawn('winlogon', proton_command(compat / 'winlogon.exe'))
    token = secrets.token_hex(32)
    ready_file = root / 'runtime/x11-input.port'
    ready_file.unlink(missing_ok=True)
    env['UURB_X11_INPUT_TOKEN'] = token
    spawn('x11-input', [str(compat / 'uu-x11-input'), '--ready-file', str(ready_file)])
    wait_until(ready_file.exists, 'input helper')
    env['UURB_X11_INPUT_PORT'] = ready_file.read_text().strip()
    spawn('input-broker', proton_command(compat / 'uu-input-broker.exe'))
    time.sleep(2)
    injected = False
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline and running:
        result = subprocess.run(proton_command(compat / 'uu-injector.exe',
                     compat / 'uu-input-bridge.dll'), env=env, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, timeout=15)
        with (root / 'logs/input-injector.log').open('ab') as output:
            output.write(result.stdout)
        if result.returncode == 0:
            injected = True
            break
        time.sleep(1)
    if not injected:
        raise RuntimeError('UU server did not accept the input bridge.')
    # Bridge FreeRDP's real cursor image, size and hotspot into Wine's reader.
    cursor_file = root / 'runtime/native-cursor.cur'
    cursor_file.unlink(missing_ok=True)
    spawn('native-cursor', ['/usr/bin/python3', '-B',
                           str(Path(__file__).with_name('uu-steamos-cursor.py'))],
          {**env, 'DISPLAY': physical_env['UURB_HOST_DISPLAY']} if gamescope else env)
    wait_until(cursor_file.exists, 'native RDP cursor image')
    (compat / 'uu-cursor.ini').write_text('[Cursor]\nSize=32\n'
        f'NativeCursorPath=Z:{str(cursor_file).replace(chr(47), chr(92))}\n')
    run(proton_command(compat / 'uu-injector.exe', compat / 'uu-cursor-guard.dll',
                       'GameViewerServer.exe'))
    for window in window_ids():
        run(['xdotool', 'windowraise', window, 'windowfocus', window])
    status = {'state': 'ready', 'relay': 'gamescope-pipewire-eis' if gamescope else 'plasma-krdp-native-freerdp',
              'session_kind': 'gamescope' if gamescope else 'plasma',
              'resolution': resolution, 'display': private_display,
              'rdp_address': None if gamescope else f'127.0.0.1:{rdp_port}',
              'prefix': str(prefix), 'proton': proton, 'input_bridge': 'injected',
              'manager': 'native-proton-xwayland',
              'cursor': 'native-gamescope-xwayland-image' if gamescope else 'native-rdp-image',
              'clipboard': 'not-yet-validated', 'controller': 'host-input-devices-exposed'}
    (root / 'runtime/status.json').write_text(json.dumps(status, indent=2))
    log(f'UU server and input bridge are ready; {status["relay"]} is connected.')
    control_path = root / 'runtime/control.sock'
    control_path.unlink(missing_ok=True)
    with socket.socket(socket.AF_UNIX) as control:
        control.bind(str(control_path))
        control.listen(1)
        control.settimeout(1)
        while running:
            for name, process in workers:
                if not name.startswith('manager') and process.poll() is not None:
                    raise RuntimeError(f'{name} exited ({process.returncode}); see logs/{name}.log')
            try:
                client, _ = control.accept()
            except socket.timeout:
                continue
            with client:
                try:
                    action = client.recv(4096).decode().strip()
                except ConnectionResetError:
                    continue
                if not action:
                    continue
                if action == 'ping':
                    send_reply(client, b'Portable session is running.\n')
                elif action == 'visible':
                    send_reply(client, b'yes\n' if manager_visible() else b'no\n')
                elif action == 'open' or action.startswith('open '):
                    try:
                        context = json.loads(action[5:]) if action.startswith('open ') else {}
                        open_manager(context)
                        send_reply(client, b'Manager is visible as a native Proton window.\n')
                    except Exception as error:
                        send_reply(client, f'Manager error: {error}\n'.encode())
                elif action == 'stop':
                    send_reply(client, b'Stopping portable session.\n')
                    request_stop()
                elif action == 'screenshot':
                    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'x11grab',
                                  '-video_size', resolution, '-i', private_display, '-frames:v', '1',
                                  str(root / 'logs/relay.png')])
                    send_reply(client, b'logs/relay.png\n')
                else:
                    send_reply(client, b'Unknown command.\n')


if __name__ == '__main__':
    try:
        serve()
    except Exception as error:
        log(str(error))
        if owns_prefix:
            (root / 'runtime/status.json').write_text(json.dumps({'state': 'failed', 'error': str(error)}))
        raise
    finally:
        if owns_prefix:
            # Release remote buttons/keys while the private X server and EIS
            # connection still exist; then tear down the other workers.
            for name, process in workers:
                if name == 'gamescope-input' and process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()
            env['DISPLAY'] = private_display
            try:
                subprocess.run([str(Path(proton).parent / 'files/bin/wineserver'), '-k'],
                               env=env, timeout=10, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            except (OSError, subprocess.TimeoutExpired):
                pass
            for name, process in reversed(workers):
                if process.poll() is None:
                    process.terminate()
            for name, process in reversed(workers):
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            (root / 'runtime/control.sock').unlink(missing_ok=True)
            status_file = root / 'runtime/status.json'
            if status_file.exists():
                status = json.loads(status_file.read_text())
                if status.get('state') != 'failed':
                    status['state'] = 'stopped'
                    status_file.write_text(json.dumps(status, indent=2))
            instance_lock.close()
