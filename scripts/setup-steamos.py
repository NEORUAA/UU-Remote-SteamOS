#!/usr/bin/env python3
"""Privately extract pinned SteamOS tools, build compatibility code and install UU."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import urllib.request
from uu_steamos_desktop import write_launcher

root = Path(os.environ['UURB_STEAMOS_ROOT'])
repo = Path(__file__).resolve().parents[1]
proton = os.environ['UURB_PROTON']
prefix = Path(os.environ['WINEPREFIX'])


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def download(url, checksum, filename=None):
    destination = root / 'downloads' / (filename or url.rsplit('/', 1)[-1])
    if destination.exists() and digest(destination) == checksum:
        return destination
    temporary = destination.with_name(destination.name + '.part')
    print(f'Downloading {destination.name}', flush=True)
    with urllib.request.urlopen(url, timeout=60) as source, temporary.open('wb') as output:
        shutil.copyfileobj(source, output)
    if digest(temporary) != checksum:
        raise RuntimeError(f'SHA-256 mismatch: {temporary}')
    temporary.replace(destination)
    return destination


def run(command, **options):
    subprocess.run(list(map(str, command)), check=True, **options)


def main():
    if (root / 'runtime/control.sock').exists():
        raise SystemExit('Stop the portable session before setup.')
    with (root / 'runtime/instance.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Stop the portable session before setup.')
        configure()


def configure():
    sysroot = root / 'tools/sysroot'
    sysroot.mkdir(exist_ok=True)
    manifest_file = repo / 'patches/steamos-packages.json'
    packages = json.loads(manifest_file.read_text())
    receipt = sysroot / '.steamos-packages-sha256'
    if not receipt.exists() or receipt.read_text().strip() != digest(manifest_file):
        for package in packages['packages']:
            archive = download(package['url'], package['sha256'])
            run(['tar', '-xf', archive, '-C', sysroot])
        receipt.write_text(digest(manifest_file) + '\n')
    runtime = root / 'tools/runtime'
    runtime.mkdir(exist_ok=True)
    for package in packages['packages']:
        if any(name in package['url'] for name in ('/xorg-server-xvfb-', '/openbox-')):
            archive = download(package['url'], package['sha256'])
            run(['tar', '-xf', archive, '-C', runtime])
    mingw = packages['llvm_mingw']
    mingw_root = root / 'tools' / mingw['directory']
    if not (mingw_root / 'bin/x86_64-w64-mingw32-gcc').exists():
        archive = download(mingw['url'], mingw['sha256'], 'llvm-mingw.tar.xz')
        run(['tar', '-xf', archive, '-C', root / 'tools'])
    host_wrapper = root / 'tools/host-cc'
    host_wrapper.write_text('#!/bin/bash\n'
        f'export LD_LIBRARY_PATH={shlex.quote(str(sysroot / "usr/lib"))}\n'
        f'exec {shlex.quote(str(sysroot / "usr/bin/gcc"))} '
        f'--sysroot={shlex.quote(str(sysroot))} -B{shlex.quote(str(sysroot / "usr/bin"))}/ '
        f'-B{shlex.quote(str(sysroot / "usr/lib"))}/ "$@"\n')
    host_wrapper.chmod(0o700)
    mingw_wrapper = root / 'tools/mingw-cc'
    # Clang diagnoses an SSPI export attribute added after MinGW's declaration.
    mingw_wrapper.write_text('#!/bin/bash\n'
        f'exec {shlex.quote(str(mingw_root / "bin/x86_64-w64-mingw32-gcc"))} '
        '-Wno-dll-attribute-on-redeclaration "$@"\n')
    mingw_wrapper.chmod(0o700)
    build_env = {**os.environ,
                 'HOST_CC': str(host_wrapper),
                 'HOST_STRIP': str(sysroot / 'usr/bin/strip'),
                 'MINGW_CC': str(mingw_wrapper), 'MINGW_STRIP': str(mingw_root / 'bin/llvm-strip')}
    compat = root / 'build/compat'
    run([repo / 'scripts/build-compat.sh', compat], env=build_env)
    release_path = repo / 'patches/uu-remote-4.42.0.2770.json'
    release = json.loads(release_path.read_text())
    app = prefix / 'drive_c/Program Files/Netease/GameViewer'
    try:
        if not (prefix / 'user.reg').exists():
            run([proton, 'getcompatpath', str(root)], timeout=180)
        if not (app / 'GameViewer.exe').exists():
            installer = release['installer']
            executable = download(installer['url'], installer['sha256'], installer['filename'])
            with (root / 'logs/install.log').open('ab') as output:
                run([proton, 'runinprefix', executable, '/S'], timeout=180,
                    stdout=output, stderr=subprocess.STDOUT)
    finally:
        # Exit 1 also means there is no wineserver for an already installed,
        # stopped prefix. An idempotent setup does not need to start one.
        server = Path(proton).parent / 'files/bin/wineserver'
        for action in ('-k', '-w'):
            result = subprocess.run([str(server), action], timeout=20)
            if result.returncode not in (0, 1):
                raise RuntimeError(f'wineserver {action} failed: {result.returncode}')
    run(['python3', '-B', repo / 'scripts/patch-gameviewer.py', 'patch',
         app / 'bin/GameViewerServer.exe', '--manifest', release_path])
    health = app / 'bin/GameViewerHealthd.exe'
    backup = health.with_name(health.name + '.uu-original')
    original = release['health_monitor']['original_sha256']
    state_file = root / 'state/deployment.json'
    previous = json.loads(state_file.read_text()) if state_file.exists() else {}
    replacement = compat / 'uu-healthd-stub.exe'
    if digest(health) == original:
        if backup.exists() and digest(backup) != original:
            raise RuntimeError('Unknown health monitor backup; refusing to replace it.')
        if not backup.exists():
            shutil.copy2(health, backup)
    elif (not backup.exists() or digest(backup) != original or
          digest(health) not in (digest(replacement), previous.get('health_stub_sha256'))):
        raise RuntimeError('Unknown health monitor; refusing to replace it.')
    shutil.copy2(replacement, health)
    devcon = app / 'bin/drivers/devcon.exe'
    devcon_backup = devcon.with_name(devcon.name + '.uu-original')
    devcon_hash = '46731d6ea59dd9b63ad641c79646bb5ff64e1b877a1226536e3fe34d1ab4ee10'
    if devcon.exists():
        if digest(devcon) != devcon_hash:
            raise RuntimeError('Unknown devcon; refusing to suppress it.')
        if devcon_backup.exists():
            if digest(devcon_backup) != devcon_hash:
                raise RuntimeError('Unknown devcon backup.')
            devcon.unlink()
        else:
            devcon.rename(devcon_backup)
    elif not devcon_backup.exists() or digest(devcon_backup) != devcon_hash:
        raise RuntimeError('The suppressed devcon has no approved backup.')
    (prefix / 'compat').mkdir(exist_ok=True)
    shutil.copy2(release_path, prefix / 'compat/release-manifest.json')
    tls = root / 'tls'
    tls.mkdir(exist_ok=True)
    if not (tls / 'server.crt').exists() or not (tls / 'server.key').exists():
        with (root / 'logs/tls.log').open('ab') as output:
            run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                 '-keyout', tls / 'server.key', '-out', tls / 'server.crt',
                 '-days', '3650', '-subj', '/CN=UURemote-Loopback'],
                stdout=output, stderr=subprocess.STDOUT)
        (tls / 'server.key').chmod(0o600)
    state_file.write_text(json.dumps({'uu_version': release['version'],
                         'health_stub_sha256': digest(replacement),
                         'packages_sha256': digest(manifest_file)}, indent=2) + '\n')
    write_launcher(root, repo)
    print(f'Portable installation is ready in {root}', flush=True)


if __name__ == '__main__':
    main()
