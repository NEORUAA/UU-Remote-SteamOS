#!/usr/bin/python3
"""Run an optional capture backend with the same installed Plus base in a lab."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
REAL_HOME = Path.home()
LIVE_PREFIX = REAL_HOME / '.local/share/wineprefixes/uu-remote'
BUS = 'unix:path=/run/user/1000/bus'


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['cp', '-a', '--reflink=auto', str(source), str(destination)], check=True)


def prepare(lab):
    os.umask(0o077)
    if (lab / 'base.json').exists():
        return
    if lab.exists():
        raise RuntimeError('Choose an empty lab directory')
    lab.mkdir(parents=True)
    prefix = lab / 'prefix'
    copy(LIVE_PREFIX, prefix)
    for name in ['uu-remote-bridge', 'uu-remote', 'uu-remote-console', 'uu-shared-physical-vnc',
                 'uu-keyring-unlock']:
        path = Path('.local/bin') / name
        copy(REAL_HOME / path, lab / 'home' / path)
    for name in ['uu-remote-stop-wine-prefix', 'uu-clean-wine-device-registry',
                 'uu-inspect-wine-device-registry.py', 'uu-connection-status',
                 'uu-cursor-asset.py', 'uu-quality.py', 'uu-clipboard-native.py', 'uu-desktop-tool.py']:
        path = Path('.local/libexec') / name
        copy(REAL_HOME / path, lab / 'home' / path)
    copy(REAL_HOME / '.local/share/uu-remote/tools', lab / 'home/.local/share/uu-remote/tools')
    settings = (REAL_HOME / '.config/uu-remote-bridge/environment').read_text().splitlines()
    settings = [s for s in settings if not s.startswith('UURB_WINEPREFIX=')]
    settings.append('UURB_WINEPREFIX=' + str(prefix))
    config = lab / 'home/.config/uu-remote-bridge'
    config.mkdir(parents=True)
    (config / 'environment').write_text('\n'.join(settings) + '\n')
    (lab / 'base.json').write_text(json.dumps({'base_version': '0.2.0-work',
        'installed_source_digest': (LIVE_PREFIX / 'compat/.runtime-source-sha256').read_text().strip(),
        'source_commit': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        'shared_features': ['UU4.42', 'Wine11', 'legacy input', 'RDP input relay',
                            'terminal persistence', 'bitmap clipboard', 'single-file clipboard'],
        'source_prefix': str(LIVE_PREFIX), 'lab_prefix': str(prefix)}) + '\n')
    print(f'Prepared the common Plus base at {lab}; account state stays private in this lab.')


def wait(check, process, seconds=60):
    deadline = time.monotonic() + seconds
    while not check():
        if process.poll() is not None:
            raise RuntimeError('Owned worker exited before readiness')
        if time.monotonic() > deadline:
            raise TimeoutError('Owned worker readiness timed out')
        time.sleep(0.1)


def run(args):
    lab = args.lab.resolve()
    prefix = lab / 'prefix'
    if not (lab / 'base.json').is_file() or prefix.resolve() == LIVE_PREFIX.resolve():
        raise RuntimeError('Prepare a private Plus lab first')
    runtime = Path('/run/user/1000/uurb-native-lab')
    runtime.mkdir(mode=0o700)
    env = {**os.environ, 'HOME': str(lab / 'home'), 'XDG_RUNTIME_DIR': str(runtime),
           'XDG_STATE_HOME': str(lab / 'state'), 'DBUS_SESSION_BUS_ADDRESS': BUS,
           'WINEPREFIX': str(prefix), 'UURB_WINEPREFIX': str(prefix), 'WINEDEBUG': '-all'}
    for line in (lab / 'home/.config/uu-remote-bridge/environment').read_text().splitlines():
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env[key] = value
    for key in ['XDG_STATE_HOME', 'XDG_RUNTIME_DIR']:
        env[key] = str(lab / 'state') if key == 'XDG_STATE_HOME' else str(runtime)
    stage = ROOT / ('build/native-' + args.backend)
    capture = ROOT / 'scripts/uu-native-capture.py'
    worker = stage / ('plus-pw-' + args.backend)
    selected = runtime / args.backend
    selected.mkdir(mode=0o700)
    command = ['/usr/bin/python3', str(capture), '--backend', args.backend, '--worker', str(worker),
               '--runtime', str(selected)]
    dll = stage / ('plus-' + args.backend + '-capture.dll')
    if args.backend == 'cpu':
        frame = selected / 'frames.v1'
        env['UURB_NATIVE_FRAME_PATH'] = 'Z:' + str(frame)
        (prefix / 'drive_c/uurb-native-video.ini').write_text('frame_path=' + env['UURB_NATIVE_FRAME_PATH'] + '\n')
    else:
        for name in ['d3d11.dll', 'dxgi.dll']:
            destination = prefix / 'drive_c/windows/system32' / name
            destination.unlink(missing_ok=True)
            copy(stage / name, destination)
        endpoint = selected / 'capture.sock'
        env.update(WINEDLLOVERRIDES='mscoree,mshtml=;d3d11,dxgi=n',
                   UURB_NATIVE_GPU_SOCKET=str(endpoint),
                   UURB_NATIVE_GPU_LOADER='Z:' + str(stage / 'uurb-dxgi-capture-loader.dll'))
        config = selected / 'dxvk.conf'
        config.write_text('dxgi.hideNvidiaGpu = False\n')
        env['DXVK_CONFIG_FILE'] = str(config)
        command += ['--gpu-socket', str(endpoint)]
    processes = []
    logs = lab / 'logs'
    logs.mkdir(exist_ok=True)
    try:
        with (logs / (args.backend + '-capture.log')).open('w') as log:
            producer = subprocess.Popen(command, env=env, stdout=log, stderr=log, start_new_session=True)
            processes.append(producer)
        wait(lambda: (selected / 'frames.v1').exists() if args.backend == 'cpu'
             else (selected / 'capture.sock').exists(), producer, 120)
        with (logs / (args.backend + '-bridge.log')).open('w') as log:
            bridge = subprocess.Popen([str(lab / 'home/.local/bin/uu-remote-bridge')], env=env,
                                      stdout=log, stderr=log, start_new_session=True)
            processes.append(bridge)
        injector = prefix / 'compat/uu-injector.exe'
        injected = False
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline and bridge.poll() is None:
            result = subprocess.run(['/opt/wine-stable/bin/wine', str(injector), 'Z:' + str(dll),
                                     'GameViewerServer.exe'], env=env, capture_output=True, timeout=10)
            if result.returncode == 0:
                injected = True
                break
            time.sleep(0.25)
        if not injected:
            raise RuntimeError('Capture adapter did not attach to the private UU process')
        (lab / 'RUNNING.json').write_text(json.dumps({'backend': args.backend, 'prefix': str(prefix),
            'producer_pid': producer.pid, 'bridge_pid': bridge.pid,
            'common_base': json.loads((lab / 'base.json').read_text()),
            'controller_tested': False, 'logs': str(logs)}) + '\n')
        print(f'{args.backend} native capture attached to the private Plus base; logs: {logs}', flush=True)
        bridge.wait(timeout=args.seconds)
    except subprocess.TimeoutExpired:
        pass
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
        subprocess.run(['/opt/wine-stable/bin/wineserver', '-k'], env=env, timeout=5,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for path in [selected, runtime / 'uu-remote-bridge']:
            if path.exists():
                import shutil
                shutil.rmtree(path)
        runtime.rmdir()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--lab', type=Path, required=True)
    parser.add_argument('--backend', choices=['cpu', 'gpu'])
    parser.add_argument('--seconds', type=int, default=12)
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare(args.lab.resolve())
    else:
        if not args.backend:
            parser.error('run requires --backend')
        run(args)


if __name__ == '__main__':
    main()
