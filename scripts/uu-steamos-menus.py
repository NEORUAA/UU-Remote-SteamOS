#!/usr/bin/env python3
"""Give UU's ownerless Qt menus the fullscreen viewer's stacking layer."""
import ctypes
import os
from pathlib import Path
import time


def menu_owner(window, windows):
    """Only repair ownerless tool menus belonging to a fullscreen UU process."""
    states = window['states']
    if window['owner'] or not {'above', 'skip_taskbar', 'skip_pager'} <= states:
        return None
    candidates = [item for item in windows if item['pid'] == window['pid']
                  and item['uu'] and 'fullscreen' in item['states']
                  and 'hidden' not in item['states']]
    return candidates[-1]['id'] if candidates else None


def main():
    x = ctypes.CDLL('libX11.so.6')
    display_type, window_type = ctypes.c_void_p, ctypes.c_ulong
    x.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x.XOpenDisplay.restype = display_type
    x.XDefaultRootWindow.argtypes = [display_type]
    x.XDefaultRootWindow.restype = window_type
    x.XInternAtom.argtypes = [display_type, ctypes.c_char_p, ctypes.c_int]
    x.XInternAtom.restype = window_type
    x.XGetWindowProperty.argtypes = [display_type, window_type, window_type,
        ctypes.c_long, ctypes.c_long, ctypes.c_int, window_type,
        ctypes.POINTER(window_type), ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(window_type), ctypes.POINTER(window_type),
        ctypes.POINTER(ctypes.c_void_p)]
    x.XFree.argtypes = [ctypes.c_void_p]
    x.XSetTransientForHint.argtypes = [display_type, window_type, window_type]
    x.XDeleteProperty.argtypes = [display_type, window_type, window_type]
    x.XSync.argtypes = [display_type, ctypes.c_int]
    # Qt menus can disappear between enumeration and a property request.
    error_type = ctypes.CFUNCTYPE(ctypes.c_int, display_type, ctypes.c_void_p)
    ignore_error = error_type(lambda *_: 0)
    x.XSetErrorHandler.argtypes = [error_type]
    x.XSetErrorHandler(ignore_error)
    display = x.XOpenDisplay(None)
    if not display:
        raise RuntimeError('The UU manager display is unavailable')
    root = x.XDefaultRootWindow(display)
    atoms = {}

    def atom(name):
        if name not in atoms:
            atoms[name] = x.XInternAtom(display, name.encode(), 0)
        return atoms[name]

    def property32(window, name):
        kind, form = window_type(), ctypes.c_int()
        count, remaining, data = window_type(), window_type(), ctypes.c_void_p()
        x.XGetWindowProperty(display, window, atom(name), 0, 4096, 0, 0,
            ctypes.byref(kind), ctypes.byref(form), ctypes.byref(count),
            ctypes.byref(remaining), ctypes.byref(data))
        try:
            if form.value != 32 or not data:
                return []
            return list(ctypes.cast(data, ctypes.POINTER(window_type))[:count.value])
        finally:
            if data:
                x.XFree(data)

    names = ('above', 'skip_taskbar', 'skip_pager', 'fullscreen', 'hidden')
    state_atoms = {atom('_NET_WM_STATE_' + name.upper()): name for name in names}
    executable = str(Path(os.environ['WINEPREFIX']) /
                     'drive_c/Program Files/Netease/GameViewer/bin/GameViewer.exe')
    repaired = {}
    processes = {}
    while True:
        windows = []
        for window in property32(root, '_NET_CLIENT_LIST_STACKING'):
            pid = next(iter(property32(window, '_NET_WM_PID')), 0)
            try:
                identity = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
                cached = processes.get((pid, identity))
                if cached is None or time.monotonic() - cached[0] > 2:
                    matched = any(line.endswith(' ' + executable) for line in
                                  Path(f'/proc/{pid}/maps').read_text().splitlines())
                    cached = processes[(pid, identity)] = (time.monotonic(), matched)
                matched = cached[1]
            except (OSError, IndexError):
                matched = False
            windows.append({'id': window, 'pid': pid, 'uu': matched,
                'states': {state_atoms[value] for value in property32(window, '_NET_WM_STATE')
                           if value in state_atoms},
                'owner': next(iter(property32(window, 'WM_TRANSIENT_FOR')), None)})
        live = {item['id']: item for item in windows}
        for window, owner in list(repaired.items()):
            item = live.get(window)
            if not item or item['owner'] != owner:
                del repaired[window]
            elif owner not in live or 'fullscreen' not in live[owner]['states']:
                x.XDeleteProperty(display, window, atom('WM_TRANSIENT_FOR'))
                item['owner'] = None
                del repaired[window]
        for item in windows:
            owner = menu_owner(item, windows)
            if owner:
                x.XSetTransientForHint(display, item['id'], owner)
                repaired[item['id']] = owner
                print(f"Attached fullscreen menu {item['id']:#x} to {owner:#x}", flush=True)
        x.XSync(display, 0)
        processes = {key: value for key, value in processes.items()
                     if time.monotonic() - value[0] < 3}
        time.sleep(0.1)


if __name__ == '__main__':
    main()
