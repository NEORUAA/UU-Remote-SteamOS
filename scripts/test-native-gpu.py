#!/usr/bin/python3
"""Fixed-4K GPU texture/encoder probe in an owned prefix; no live UU changes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / '.omc/artifacts/native-45-compare-20261004'
WINE = '/opt/wine-stable/bin/wine'


def main():
    with tempfile.TemporaryDirectory(prefix='uurb-native-gpu-') as name:
        lab = Path(name)
        env = {**os.environ, 'WINEPREFIX': str(lab / 'prefix'), 'WINEDEBUG': '-all',
               'WINEDLLOVERRIDES': 'mscoree,mshtml='}
        xvfb = None
        try:
            xvfb = subprocess.Popen(['Xvfb', '-displayfd', '1', '-screen', '0',
                                      '3840x2160x24', '-nolisten', 'tcp'],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            env['DISPLAY'] = ':' + xvfb.stdout.readline().strip()
            subprocess.run([WINE, 'wineboot', '-u'], env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=40, check=True)
            system32 = lab / 'prefix/drive_c/windows/system32'
            for name in ['d3d11.dll', 'dxgi.dll']:
                target = system32 / name
                target.unlink(missing_ok=True)
                shutil.copy2(ROOT / 'build/native-gpu' / name, target)
            env['WINEDLLOVERRIDES'] = 'mscoree,mshtml=;d3d11,dxgi=n'
            config = lab / 'dxvk.conf'
            config.write_text('dxgi.hideNvidiaGpu = False\n')
            env['DXVK_CONFIG_FILE'] = str(config)
            output = lab / 'frames'
            output.mkdir()
            probe = ROOT / 'build/native-gpu/plus-gpu-interop-probe.exe'
            with (ART / 'GPU-INTEROP-LOG.txt').open('w') as log:
                result = subprocess.run([str(probe), str(output), 'sequence', '3840', '2160', '5'],
                                        env=env, stdout=log, stderr=log, timeout=45)
            report = {'exit_code': result.returncode, 'width': 3840, 'height': 2160,
                      'frames': 5, 'log': str(ART / 'GPU-INTEROP-LOG.txt'),
                      'output_files': {p.name: p.stat().st_size for p in output.iterdir()},
                      'scope': 'synthetic D3D11/Vulkan/CUDA/NVENC; no portal DMA-BUF or UU controller acceptance'}
            if result.returncode == 0:
                for p in output.iterdir():
                    if p.name in ('h264.bin', 'hevc.bin', 'frames.jsonl'):
                        shutil.copy2(p, ART / ('GPU-PROBE-' + p.name))
            print(json.dumps(report, indent=2))
            if result.returncode:
                raise RuntimeError(f'GPU interop failed: inspect {report["log"]}')
        finally:
            subprocess.run(['/opt/wine-stable/bin/wineserver', '-k'], env=env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            if xvfb:
                xvfb.terminate()
                xvfb.wait(timeout=5)


if __name__ == '__main__':
    main()
