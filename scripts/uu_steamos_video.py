#!/usr/bin/env python3
"""Prepare hash-reviewed, installation-local Proton video compatibility copies."""
import hashlib
import json
import math
from pathlib import Path
import re
import struct


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def reviewed(data, expected, name):
    if sha256(data) != expected:
        raise RuntimeError(f'Unreviewed {name}; refusing video compatibility patches.')


def sections(data):
    pe = struct.unpack_from('<I', data, 60)[0]
    if data[pe:pe + 4] != b'PE\0\0':
        raise RuntimeError('Invalid PE image.')
    machine, count = struct.unpack_from('<HH', data, pe + 4)
    size = struct.unpack_from('<H', data, pe + 20)[0]
    optional = pe + 24
    if machine != 0x8664 or struct.unpack_from('<H', data, optional)[0] != 0x20b:
        raise RuntimeError('Video patches require an AMD64 PE32+ image.')
    table = optional + size
    entries = []
    for index in range(count):
        offset = table + index * 40
        virtual_size, rva, raw_size, raw = struct.unpack_from('<4I', data, offset + 8)
        entries.append((rva, virtual_size, raw, raw_size))
    return pe, optional, table, entries


def rva_offset(rva, entries):
    for start, virtual_size, raw, raw_size in entries:
        if start <= rva < start + min(virtual_size, raw_size):
            return raw + rva - start
    raise RuntimeError(f'PE RVA {rva:#x} has no file-backed section.')


def native_marker(data):
    # Wine redirects files carrying this marker back to its installed builtin.
    # These private PE copies retain the Wine implementations and dependencies.
    if data[64:80] != b'Wine builtin DLL':
        raise RuntimeError('Unexpected Proton builtin marker.')
    data[64:80] = b'UU video shim   '


def patch_d3d11(original, spec):
    reviewed(original, spec['sha256'], 'Proton d3d11.dll')
    data = bytearray(original)
    pe, optional, table, entries = sections(data)
    alignment = struct.unpack_from('<I', data, optional + 32)[0]
    file_alignment = struct.unpack_from('<I', data, optional + 36)[0]
    align = lambda value, boundary: (value + boundary - 1) // boundary * boundary
    rva = align(struct.unpack_from('<I', data, optional + 56)[0], alignment)
    payload = bytearray()
    new_functions = []
    replacements = {}
    for patch in spec['patches']:
        old_rva = int(patch['rva'], 16)
        offset = rva_offset(old_rva, entries)
        expected = bytes.fromhex(patch['original'])
        if data[offset:offset + len(expected)] != expected or len(expected) != 5:
            raise RuntimeError('Unexpected video query function prologue.')
        target = rva + len(payload)
        code = bytes.fromhex(patch['code'])
        payload.extend(code)
        payload.extend(b'\x90' * (-len(payload) % 4))
        unwind_rva = rva + len(payload)
        payload.extend(bytes.fromhex(patch['unwind']))
        new_functions.append((target, target + len(code), unwind_rva))
        replacements[old_rva] = None
        data[offset:offset + 5] = b'\xe9' + struct.pack('<i', target - old_rva - 5)
        payload.extend(b'\0' * (-len(payload) % 16))
    leaf_unwind = rva + len(payload)
    payload.extend(b'\x01\0\0\0')
    # Preserve unwind information for appended helpers and make each replaced
    # entry's five-byte jump a leaf. The old function bodies are unreachable.
    exception_rva, exception_size = struct.unpack_from('<II', data, optional + 112 + 3 * 8)
    if not exception_size or exception_size % 12:
        raise RuntimeError('Unexpected Proton exception directory.')
    exception_offset = rva_offset(exception_rva, entries)
    functions = []
    for offset in range(exception_offset, exception_offset + exception_size, 12):
        begin, end, unwind = struct.unpack_from('<III', data, offset)
        if begin in replacements:
            end, unwind = begin + 5, leaf_unwind
            replacements[begin] = True
        functions.append((begin, end, unwind))
    if not all(replacements.values()):
        raise RuntimeError('Missing video query unwind entries.')
    payload.extend(b'\0' * (-len(payload) % 4))
    new_exception_rva = rva + len(payload)
    for function in sorted(functions + new_functions):
        payload.extend(struct.pack('<III', *function))
    struct.pack_into('<II', data, optional + 112 + 3 * 8,
                     new_exception_rva, (len(functions) + len(new_functions)) * 12)
    header = table + len(entries) * 40
    headers_size = struct.unpack_from('<I', data, optional + 60)[0]
    if header + 40 > headers_size or any(data[header:header + 40]):
        raise RuntimeError('No unused PE section header available.')
    raw = align(len(data), file_alignment)
    raw_size = align(len(payload), file_alignment)
    data.extend(b'\0' * (raw - len(data)))
    data.extend(payload)
    data.extend(b'\0' * (raw_size - len(payload)))
    data[header:header + 8] = b'.uurb\0\0\0'
    struct.pack_into('<4I', data, header + 8, len(payload), rva, raw_size, raw)
    struct.pack_into('<I', data, header + 36, 0x60000020)
    struct.pack_into('<H', data, pe + 6, len(entries) + 1)
    struct.pack_into('<I', data, optional + 56, align(rva + len(payload), alignment))
    struct.pack_into('<I', data, optional + 64, 0)
    native_marker(data)
    return bytes(data)


def patch_bytes(original, spec, name, builtin=False):
    reviewed(original, spec.get('sha256', spec.get('original_sha256')), name)
    offset = spec['file_offset']
    before, after = bytes.fromhex(spec['original']), bytes.fromhex(spec['replacement'])
    if len(before) != len(after) or original[offset:offset + len(before)] != before:
        raise RuntimeError(f'Unexpected {name} patch bytes.')
    data = bytearray(original)
    data[offset:offset + len(before)] = after
    if builtin:
        native_marker(data)
    return bytes(data)


def write_managed(path, data):
    if path.is_symlink():
        raise RuntimeError(f'Refusing symlinked video output: {path}')
    if path.is_file() and path.read_bytes() == data:
        return
    temporary = path.with_name(path.name + '.tmp')
    if temporary.is_symlink():
        raise RuntimeError('Refusing symlinked temporary video output.')
    temporary.write_bytes(data)
    temporary.chmod(0o600)
    temporary.replace(path)


def display_refresh(xrandr_output):
    """Read active host modes, avoiding the zero-Hz private Xvfb display."""
    rates = [float(match.group(1)) for match in
             re.finditer(r'(?<!\S)(\d+(?:\.\d+)?)\*', xrandr_output)]
    rates = [rate for rate in rates if 1 <= rate <= 1000]
    if not rates:
        raise RuntimeError('Cannot determine the active host display refresh rate.')
    return math.floor(max(rates) + 0.5)


def patch_refresh(original, spec, refresh):
    """Seed UU's local display limit from the host instead of zero-Hz Wine modes.

    UU still clamps the user's requested rate and considers valid Wine modes.
    Only this reviewed instruction's immediate may differ on subsequent runs.
    """
    if not isinstance(refresh, int) or isinstance(refresh, bool) or not 1 <= refresh <= 1000:
        raise RuntimeError('Invalid host display refresh rate.')
    offset = spec['file_offset']
    before = bytes.fromhex(spec['original'])
    if len(before) != 5 or original[offset:offset + 1] != before[:1]:
        raise RuntimeError('Unexpected UU display-limit instruction.')
    previous = struct.unpack_from('<I', original, offset + 1)[0]
    if not 1 <= previous <= 1000:
        raise RuntimeError('Unexpected existing UU display limit.')
    data = bytearray(original)
    data[offset:offset + 5] = before
    reviewed(data, spec['sha256'], 'UU display-limit client')
    struct.pack_into('<I', data, offset + 1, refresh)
    return bytes(data)


def prepare(root, proton, app, refresh=None):
    manifest = json.loads(Path(__file__).resolve().parents[1].joinpath(
        'patches/steamos-video.json').read_text())
    output = root / 'build/compat'
    source = proton.parent / 'files/lib/wine/x86_64-windows'
    if not output.parent.resolve().is_relative_to(root.resolve()):
        raise RuntimeError('Video outputs must stay inside the installation.')
    output.mkdir(parents=True, exist_ok=True)
    if not output.resolve().is_relative_to(root.resolve()):
        raise RuntimeError('Video output directory cannot escape the installation.')
    generated, links = [], []
    for filename, key, transform in (
            ('d3d11', 'd3d11', patch_d3d11),
            ('wined3d', 'wined3d', lambda data, spec: patch_bytes(data, spec, 'Proton wined3d.dll', True))):
        original = (source / (filename + '.dll')).read_bytes()
        destination = output / (filename + '-video.dll')
        link = app / 'bin' / (filename + '.dll')
        if link.is_symlink():
            if link.readlink() != destination:
                raise RuntimeError(f'Unmanaged application DLL link: {link}')
        elif link.exists():
            raise RuntimeError(f'Existing application DLL must be preserved: {link}')
        generated.append((destination, transform(original, manifest[key])))
        links.append((link, destination))
    for filename, key in (('streamer.dll', 'streamer'), ('StreamerCodecDetector.exe', 'detector')):
        path = app / 'bin' / filename
        data = path.read_bytes()
        spec = manifest[key]
        if sha256(data) == spec['patched_sha256']:
            continue
        patched = patch_bytes(data, spec, filename)
        reviewed(patched, spec['patched_sha256'], 'patched ' + filename)
        generated.append((path, patched))
    if refresh is not None:
        client = app / 'bin/GameViewer.exe'
        if client.is_symlink():
            raise RuntimeError('Refusing symlinked UU display-limit client.')
        generated.append((client, patch_refresh(client.read_bytes(), manifest['client_refresh'], refresh)))
    # Validate every input and link before changing any application files.
    for path, data in generated:
        write_managed(path, data)
    for link, destination in links:
        if not link.is_symlink():
            link.symlink_to(destination)
