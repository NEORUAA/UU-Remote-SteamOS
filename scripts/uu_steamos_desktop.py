#!/usr/bin/env python3
"""Launch the portable manager with visible errors and a root-local log."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def desktop_quote(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%') + '"'


def write_launcher(root, repo):
    launcher = root / 'UU Remote.desktop'
    launcher.write_text('[Desktop Entry]\nType=Application\nName=UU Remote\n'
        'Comment=Run UU Remote with Steam Proton in Desktop or Gaming Mode\n'
        f'Exec=/usr/bin/python3 -B {desktop_quote(repo / "scripts/uu_steamos_desktop.py")} '
        f'--root {desktop_quote(root)}\n'
        f'Path={root}\nIcon={repo / "docs/images/uu-plus-logo.png"}\n'
        'Terminal=false\nStartupNotify=false\nCategories=Network;RemoteAccess;\n')
    launcher.chmod(0o700)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--write-launcher', action='store_true')
    args = parser.parse_args()
    root = args.root.expanduser().absolute()
    repo = Path(__file__).resolve().parents[1]
    if args.write_launcher:
        write_launcher(root, repo)
        return 0
    (root / 'logs').mkdir(parents=True, exist_ok=True)
    log = root / 'logs/launcher.log'
    with log.open('ab', buffering=0) as output:
        result = subprocess.run([sys.executable, '-B', str(repo / 'scripts/uu-steamos'),
                                 '--root', str(root), 'open'], stdout=output,
                                stderr=subprocess.STDOUT)
    if result.returncode:
        subprocess.run(['kdialog', '--title', 'UU Remote', '--error',
                        f'UU Remote could not start.\nSee the startup log:\n{log}'])
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
