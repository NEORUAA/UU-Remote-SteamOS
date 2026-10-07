#!/usr/bin/env python3
"""Remove build and diagnostic artifacts from a stopped portable installation."""
import fcntl
import json
import os
from pathlib import Path
import shutil

root = Path(os.environ['UURB_STEAMOS_ROOT']).resolve()


def remove(path):
    if not path.parent.resolve().is_relative_to(root):
        raise RuntimeError(f'Refusing cleanup outside installation: {path}')
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main():
    if (root / 'runtime/control.sock').exists():
        raise SystemExit('Stop UU before pruning.')
    with (root / 'runtime/instance.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Stop UU before pruning.')
        for binary in ('usr/bin/Xvfb', 'usr/bin/Xephyr', 'usr/bin/openbox', 'usr/bin/xcompmgr'):
            if not (root / 'tools/runtime' / binary).is_file():
                raise SystemExit('Run setup to prepare the compact runtime before pruning.')
        tools = root / 'tools'
        active_proton = Path(os.environ['UURB_PROTON']).parent
        for path in tools.iterdir():
            if path not in (tools / 'runtime', active_proton):
                remove(path)
        for directory in ('downloads', 'logs', 'tmp', 'shm', 'cache'):
            for path in (root / directory).iterdir():
                remove(path)
        keep = {'uu-input-bridge.dll', 'uu-cursor-guard.dll', 'uu-input-broker.exe',
                'uu-injector.exe', 'uu-healthd-stub.exe', 'winlogon.exe',
                'uu-x11-input', 'uu-krdp-input-auth.so'}
        for path in (root / 'build/compat').iterdir():
            if path.name not in keep:
                remove(path)
        for relative in ('config/tigervnc', 'config/menus', 'data/tigervnc',
                         'data/applications', 'data/desktop-directories', 'state/tigervnc'):
            remove(root / relative)
        for path in (root / 'runtime').iterdir():
            if path.name != 'instance.lock':
                remove(path)
        (root / 'state/last-cleanup.json').write_text(json.dumps({
            'retained': ['compatdata', 'config', 'tls', 'project', 'build/compat',
                         'tools/runtime', str(active_proton.relative_to(root))],
            'rebuild': 'Run setup again to download the pinned build tools.'
        }, indent=2) + '\n')
    print('Removed downloads, compilers, stale tools, caches and diagnostics; UU account preserved.')


if __name__ == '__main__':
    main()
