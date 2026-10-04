#!/usr/bin/python3
"""One isolated fixed-4K frame verifies the native CPU capture boundary."""
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WINE = '/opt/wine-stable/bin/wine'
WINE_SERVER = '/opt/wine-stable/bin/wineserver'


def main():
    with tempfile.TemporaryDirectory(prefix='uurb-native-cpu-') as name:
        lab = Path(name)
        xvfb = None
        env = {**os.environ, 'WINEPREFIX': str(lab / 'prefix'), 'WINEDEBUG': '-all',
               'WINEDLLOVERRIDES': 'mscoree,mshtml='}
        try:
            xvfb = subprocess.Popen(['Xvfb', '-displayfd', '1', '-screen', '0',
                                      '3840x2160x24', '-nolisten', 'tcp'],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            env['DISPLAY'] = ':' + xvfb.stdout.readline().strip()
            subprocess.run([WINE, 'wineboot', '-u'], env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=40, check=True)
            frame = lab / 'frames.v1'
            pixels = bytes((29, 61, 193, 0)) * (3840 * 2160)
            header = struct.pack('<IIIIIIQ', 0x46525555, 1, 3840, 2160, 3840 * 4, 1, 1) + bytes(32)
            with frame.open('wb') as out:
                out.write(header)
                for slot in range(3):
                    out.write(struct.pack('<Q', 2 if slot == 1 else 0))
                    out.write(pixels)
            env['UURB_NATIVE_FRAME_PATH'] = 'Z:' + str(frame)
            dll = lab / 'plus-cpu-capture.dll'
            shutil.copy2(ROOT / 'build/native-cpu/plus-cpu-capture.dll', dll)
            probe = lab / 'consumer.exe'
            subprocess.run(['x86_64-w64-mingw32-gcc', '-std=c11', '-O2', '-Wall', '-Wextra',
                            '-Werror', '-Wl,--no-insert-timestamp', '-o', str(probe),
                            str(ROOT / 'tests/probes/uu_native_cpu_consumer.c'), '-lgdi32', '-luser32'],
                           check=True)
            result = subprocess.run([WINE, str(probe), 'Z:' + str(dll)], env=env,
                                     capture_output=True, text=True, timeout=30)
            if result.returncode:
                raise RuntimeError(f'Consumer failed with {result.returncode}: {result.stderr[-1800:]}')
            data = json.loads(result.stdout)
            data['owned_lab_resources_cleaned'] = True
            print(json.dumps(data, indent=2))
        finally:
            subprocess.run([WINE_SERVER, '-k'], env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=5)
            if xvfb:
                xvfb.terminate()
                xvfb.wait(timeout=5)


if __name__ == '__main__':
    main()
