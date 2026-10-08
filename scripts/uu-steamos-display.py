#!/usr/bin/python3 -B
"""Publish the native nested compositor's Xwayland environment."""
import ctypes
import json
import os
from pathlib import Path
import runpy
import signal


def main():
    # Exit with KWin even if its session child is orphaned during shutdown.
    parent = os.getppid()
    ctypes.CDLL(None).prctl(1, signal.SIGTERM, 0, 0, 0)
    if os.getppid() != parent:
        return
    root = Path(os.environ['UURB_STEAMOS_ROOT'])
    ready = root / 'runtime/manager-display.json'
    data = {name: os.environ[name] for name in ('DISPLAY', 'XAUTHORITY') if name in os.environ}
    if not data.get('DISPLAY'):
        raise RuntimeError('KWin did not provide an Xwayland display')
    temporary = ready.with_suffix('.tmp')
    temporary.write_text(json.dumps(data))
    temporary.chmod(0o600)
    temporary.replace(ready)
    runpy.run_path(str(Path(__file__).with_name('uu-steamos-menus.py')), run_name='__main__')


if __name__ == '__main__':
    main()
