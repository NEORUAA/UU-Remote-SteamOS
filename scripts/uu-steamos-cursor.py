#!/usr/bin/env python3
"""Publish the native RDP X cursor as an atomic Windows CUR image."""
import ctypes
import os
from pathlib import Path
import struct
import time


class CursorImage(ctypes.Structure):
    _fields_ = [('x', ctypes.c_short), ('y', ctypes.c_short),
                ('width', ctypes.c_ushort), ('height', ctypes.c_ushort),
                ('xhot', ctypes.c_ushort), ('yhot', ctypes.c_ushort),
                ('serial', ctypes.c_ulong), ('pixels', ctypes.POINTER(ctypes.c_ulong))]


def encode_cursor(width, height, xhot, yhot, pixels):
    if not (1 <= width <= 128 and 1 <= height <= 128
            and 0 <= xhot < width and 0 <= yhot < height and len(pixels) == width * height):
        raise ValueError('Invalid native cursor dimensions')
    color = b''.join(struct.pack('<I', pixel & 0xffffffff)
                     for row in range(height - 1, -1, -1)
                     for pixel in pixels[row * width:(row + 1) * width])
    stride = ((width + 31) // 32) * 4
    mask = bytearray(stride * height)
    for row in range(height):
        for column in range(width):
            if (pixels[(height - row - 1) * width + column] >> 24) == 0:
                mask[row * stride + column // 8] |= 1 << (7 - column % 8)
    dib = struct.pack('<IiiHHIIiiII', 40, width, height * 2, 1, 32, 0,
                      len(color) + len(mask), 0, 0, 0, 0) + color + mask
    return (struct.pack('<HHH', 0, 2, 1)
            + struct.pack('<BBBBHHII', width, height, 0, 0, xhot, yhot, len(dib), 22) + dib)


def encode_native_cursor(image):
    if not image.width or not image.height:
        return encode_cursor(1, 1, 0, 0, [0])
    if image.width > 128 or image.height > 128:
        return None
    return encode_cursor(image.width, image.height,
                         min(image.xhot, image.width - 1),
                         min(image.yhot, image.height - 1),
                         list(image.pixels[:image.width * image.height]))


def main():
    destination = Path(os.environ['UURB_STEAMOS_ROOT']) / 'runtime/native-cursor.cur'
    x11 = ctypes.CDLL('libX11.so.6')
    fixes = ctypes.CDLL('libXfixes.so.3')
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    x11.XFree.argtypes = [ctypes.c_void_p]
    x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    x11.XDefaultRootWindow.restype = ctypes.c_ulong
    x11.XInternAtom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
    x11.XInternAtom.restype = ctypes.c_ulong
    x11.XGetWindowProperty.argtypes = [ctypes.c_void_p, ctypes.c_ulong,
        ctypes.c_ulong, ctypes.c_long, ctypes.c_long, ctypes.c_int, ctypes.c_ulong,
        ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong),
        ctypes.POINTER(ctypes.c_void_p)]
    fixes.XFixesGetCursorImage.argtypes = [ctypes.c_void_p]
    fixes.XFixesGetCursorImage.restype = ctypes.POINTER(CursorImage)
    display = x11.XOpenDisplay(None)
    if not display:
        raise RuntimeError('The private X display is unavailable')
    hosts = {os.environ.get('DISPLAY', ':0'): display}
    gamescope = os.environ.get('UURB_SESSION_KIND') == 'gamescope'
    if gamescope:
        for name in os.environ.get('UURB_HOST_DISPLAYS', '').split(','):
            if name and name not in hosts:
                secondary = x11.XOpenDisplay(os.fsencode(name))
                if secondary:
                    hosts[name] = secondary
    focus_atom = x11.XInternAtom(display, b'GAMESCOPE_MOUSE_FOCUS_DISPLAY', 0)
    last = None
    while True:
        selected = display
        if gamescope:
            kind, form, count, after, data = ctypes.c_ulong(), ctypes.c_int(), ctypes.c_ulong(), ctypes.c_ulong(), ctypes.c_void_p()
            x11.XGetWindowProperty(display, x11.XDefaultRootWindow(display), focus_atom,
                0, 1, 0, 0, ctypes.byref(kind), ctypes.byref(form), ctypes.byref(count),
                ctypes.byref(after), ctypes.byref(data))
            try:
                if form.value == 32 and count.value:
                    # Gamescope publishes its short display name in CARDINALs.
                    value = ctypes.cast(data, ctypes.POINTER(ctypes.c_ulong))[0]
                    name = (value & 0xffffffff).to_bytes(4, 'little').split(b'\0')[0].decode()
                    selected = hosts.get(name, display)
            finally:
                if data:
                    x11.XFree(data)
        pointer = fixes.XFixesGetCursorImage(selected)
        if not pointer:
            raise RuntimeError('XFixes did not provide a cursor')
        try:
            image = pointer.contents
            identity = (selected, image.serial)
            if identity != last:
                # Steam/gamescope can publish a zero-sized hidden cursor.
                # Publish transparency instead of killing the whole session.
                # Tiny transparent cursors may retain a previous stale hotspot.
                data = encode_native_cursor(image)
                if data is None:
                    last = identity
                    print(f'Skipping oversized cursor: {image.width}x{image.height}', flush=True)
                    time.sleep(0.05)
                    continue
                temporary = destination.with_suffix('.part')
                temporary.write_bytes(data)
                temporary.replace(destination)
                last = identity
                print(f'Native cursor: {image.width}x{image.height}, hotspot {image.xhot},{image.yhot}', flush=True)
        finally:
            x11.XFree(pointer)
        time.sleep(0.05)


if __name__ == '__main__':
    main()
