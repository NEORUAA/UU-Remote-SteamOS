#!/usr/bin/env python3
"""Forward the private XTEST canvas to gamescope's existing libei seat."""
import ctypes as C
import os
from pathlib import Path
import select
import signal
import time


P = C.c_void_p
U = C.c_ulong
I = C.c_int


class Cookie(C.Structure):
    _fields_ = [('type', I), ('serial', U), ('send_event', I), ('display', P),
                ('extension', I), ('evtype', I), ('cookie', C.c_uint), ('data', P)]


class Event(C.Union):
    _fields_ = [('cookie', Cookie), ('padding', C.c_long * 24)]


class Valuators(C.Structure):
    _fields_ = [('mask_len', I), ('mask', C.POINTER(C.c_ubyte)),
                ('values', C.POINTER(C.c_double))]


class Raw(C.Structure):
    _fields_ = [('type', I), ('serial', U), ('send_event', I), ('display', P),
                ('extension', I), ('evtype', I), ('time', U), ('deviceid', I),
                ('sourceid', I), ('detail', I), ('flags', I),
                ('valuators', Valuators), ('raw_values', C.POINTER(C.c_double))]


class Mask(C.Structure):
    _fields_ = [('deviceid', I), ('mask_len', I), ('mask', C.POINTER(C.c_ubyte))]


def function(library, name, result, *arguments):
    value = getattr(library, name)
    value.restype = result
    value.argtypes = list(arguments)
    return value


def map_position(x, y, canvas, surface):
    """Undo gamescope's centered aspect-preserving presentation."""
    cw, ch = canvas
    sw, sh = surface
    scale = min(cw / sw, ch / sh)
    return (max(0, min(sw - 1, (x - (cw - sw * scale) / 2) / scale)),
            max(0, min(sh - 1, (y - (ch - sh * scale) / 2) / scale)))


class EI:
    def __init__(self, socket_path):
        lib = C.CDLL('libei.so.1')
        for name, result, args in (
            ('ei_new_sender', P, [P]), ('ei_configure_name', None, [P, C.c_char_p]),
            ('ei_setup_backend_socket', I, [P, C.c_char_p]), ('ei_get_fd', I, [P]),
            ('ei_dispatch', None, [P]), ('ei_get_event', P, [P]),
            ('ei_event_get_type', I, [P]), ('ei_event_type_to_string', C.c_char_p, [I]),
            ('ei_event_get_seat', P, [P]), ('ei_event_get_device', P, [P]),
            ('ei_event_unref', P, [P]), ('ei_device_ref', P, [P]),
            ('ei_device_unref', P, [P]), ('ei_device_has_capability', C.c_bool, [P, I]),
            ('ei_device_start_emulating', None, [P, C.c_uint32]),
            ('ei_device_frame', None, [P, C.c_uint64]), ('ei_now', C.c_uint64, [P]),
            ('ei_device_pointer_motion_absolute', None, [P, C.c_double, C.c_double]),
            ('ei_device_pointer_motion', None, [P, C.c_double, C.c_double]),
            ('ei_device_button_button', None, [P, C.c_uint32, C.c_bool]),
            ('ei_device_keyboard_key', None, [P, C.c_uint32, C.c_bool]),
            ('ei_device_scroll_discrete', None, [P, C.c_int32, C.c_int32]),
            ('ei_unref', P, [P])):
            function(lib, name, result, *args)
        # Varargs capabilities use enum-sized ints and a pointer-sized sentinel.
        function(lib, 'ei_seat_bind_capabilities', None, P)
        self.lib = lib
        self.context = lib.ei_new_sender(None)
        self.devices = {}
        self.keys = set()
        self.buttons = set()
        lib.ei_configure_name(self.context, b'UU Remote SteamOS')
        if lib.ei_setup_backend_socket(self.context, os.fsencode(socket_path)) != 0:
            raise RuntimeError('Cannot connect to the gamescope EIS socket')
        self.fd = lib.ei_get_fd(self.context)

    def dispatch(self):
        lib = self.lib
        lib.ei_dispatch(self.context)
        while True:
            event = lib.ei_get_event(self.context)
            if not event:
                break
            try:
                kind = lib.ei_event_get_type(event)
                if kind == 2:
                    raise RuntimeError('Gamescope disconnected its EIS seat')
                if kind == 3:
                    lib.ei_seat_bind_capabilities(lib.ei_event_get_seat(event),
                        I(1), I(2), I(4), I(16), I(32), P(None))
                if kind in (6, 7, 8):
                    device = lib.ei_event_get_device(event)
                    if kind == 8:
                        if device not in self.devices:
                            self.devices[device] = lib.ei_device_ref(device)
                        lib.ei_device_start_emulating(device, 1)
                        print('Gamescope input device resumed', flush=True)
                    elif device in self.devices:
                        lib.ei_device_unref(self.devices.pop(device))
            finally:
                lib.ei_event_unref(event)

    def send(self, capability, name, *args):
        for device in self.devices:
            if self.lib.ei_device_has_capability(device, capability):
                getattr(self.lib, name)(device, *args)
                self.lib.ei_device_frame(device, self.lib.ei_now(self.context))
                self.lib.ei_dispatch(self.context)
                return True
        return False

    def close(self):
        for key in self.keys:
            self.send(4, 'ei_device_keyboard_key', key, False)
        for button in self.buttons:
            self.send(32, 'ei_device_button_button', button, False)
        for device in self.devices.values():
            self.lib.ei_device_unref(device)
        self.lib.ei_unref(self.context)


class XInput:
    def __init__(self):
        self.x = C.CDLL('libX11.so.6')
        self.xi = C.CDLL('libXi.so.6')
        # Focus may change between querying its ID and reading its geometry.
        # Also, a window ID from one Xwayland need not exist in the other.
        error_callback = C.CFUNCTYPE(I, P, P)
        self.error_handler = error_callback(lambda *_: 0)
        function(self.x, 'XSetErrorHandler', P, error_callback)(self.error_handler)
        for name, result, args in (
            ('XOpenDisplay', P, [C.c_char_p]), ('XCloseDisplay', I, [P]),
            ('XDefaultRootWindow', U, [P]), ('XConnectionNumber', I, [P]),
            ('XPending', I, [P]), ('XNextEvent', I, [P, C.POINTER(Event)]),
            ('XGetEventData', I, [P, C.POINTER(Cookie)]),
            ('XFreeEventData', None, [P, C.POINTER(Cookie)]),
            ('XFlush', I, [P]), ('XInternAtom', U, [P, C.c_char_p, I]),
            ('XGetWindowProperty', I, [P, U, U, C.c_long, C.c_long, I, U,
                C.POINTER(U), C.POINTER(I), C.POINTER(U), C.POINTER(U), C.POINTER(P)]),
            ('XFree', I, [P]),
            ('XGetGeometry', I, [P, U, C.POINTER(U), C.POINTER(I), C.POINTER(I),
                C.POINTER(C.c_uint), C.POINTER(C.c_uint), C.POINTER(C.c_uint), C.POINTER(C.c_uint)]),
            ('XQueryPointer', I, [P, U, C.POINTER(U), C.POINTER(U), C.POINTER(I),
                C.POINTER(I), C.POINTER(I), C.POINTER(I), C.POINTER(C.c_uint)])):
            function(self.x, name, result, *args)
        function(self.xi, 'XISelectEvents', I, P, U, C.POINTER(Mask), I)
        function(self.xi, 'XIQueryVersion', I, P, C.POINTER(I), C.POINTER(I))
        self.display = self.x.XOpenDisplay(None)
        if not self.display:
            raise RuntimeError('Private input canvas is unavailable')
        self.root = self.x.XDefaultRootWindow(self.display)
        self.fd = self.x.XConnectionNumber(self.display)
        major, minor = I(2), I(2)
        if self.xi.XIQueryVersion(self.display, C.byref(major), C.byref(minor)):
            raise RuntimeError('XInput2 is unavailable')
        mask = (C.c_ubyte * 3)()
        for event in (6, 13, 14, 15, 16, 17):
            mask[event >> 3] |= 1 << (event & 7)
        selection = Mask(1, len(mask), mask)  # XIAllMasterDevices: no slave duplicates.
        self.xi.XISelectEvents(self.display, self.root, C.byref(selection), 1)
        self.x.XFlush(self.display)
        names = os.environ.get('UURB_HOST_DISPLAYS', os.environ['UURB_HOST_DISPLAY']).split(',')
        self.hosts = [self.x.XOpenDisplay(os.fsencode(name)) for name in names]
        self.hosts = [display for display in self.hosts if display]
        self.canvas = tuple(map(int, os.environ['UURB_RESOLUTION'].split('x')))
        self.surface = self.canvas
        self.deadline = 0

    def property(self, display, window, name):
        atom = self.x.XInternAtom(display, name, 0)
        kind, count, after, data, form = U(), U(), U(), P(), I()
        result = self.x.XGetWindowProperty(display, window, atom, 0, 1, 0, 0,
            C.byref(kind), C.byref(form), C.byref(count), C.byref(after), C.byref(data))
        try:
            return C.cast(data, C.POINTER(U))[0] if result == 0 and form.value == 32 and count.value else 0
        finally:
            if data:
                self.x.XFree(data)

    def position(self):
        if time.monotonic() >= self.deadline and self.hosts:
            self.deadline = time.monotonic() + 0.25
            primary = self.hosts[0]
            host_root = self.x.XDefaultRootWindow(primary)
            appid = self.property(primary, host_root, b'GAMESCOPE_FOCUSED_APP')
            window = self.property(primary, host_root, b'GAMESCOPE_FOCUSED_WINDOW')
            # Window IDs can overlap between independent Xwayland servers.
            for display in self.hosts:
                if window and self.property(display, window, b'STEAM_GAME') == appid:
                    root, x, y, w, h, border, depth = U(), I(), I(), C.c_uint(), C.c_uint(), C.c_uint(), C.c_uint()
                    if self.x.XGetGeometry(display, window, C.byref(root), C.byref(x), C.byref(y),
                        C.byref(w), C.byref(h), C.byref(border), C.byref(depth)) and w.value and h.value:
                        self.surface = (w.value, h.value)
                        break
        root, child, x, y, wx, wy, mask = U(), U(), I(), I(), I(), I(), C.c_uint()
        self.x.XQueryPointer(self.display, self.root, C.byref(root), C.byref(child),
            C.byref(x), C.byref(y), C.byref(wx), C.byref(wy), C.byref(mask))
        return map_position(x.value, y.value, self.canvas, self.surface)

    def events(self):
        while self.x.XPending(self.display):
            event = Event()
            self.x.XNextEvent(self.display, C.byref(event))
            if event.cookie.type != 35 or not self.x.XGetEventData(self.display, C.byref(event.cookie)):
                continue
            try:
                raw = C.cast(event.cookie.data, C.POINTER(Raw)).contents
                # XTEST absolute warps produce XI_Motion, not XI_RawMotion.
                yield (17 if event.cookie.evtype == 6 else raw.evtype), raw.detail
            finally:
                self.x.XFreeEventData(self.display, C.byref(event.cookie))


def main():
    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    ei = EI(os.environ['UURB_GAMESCOPE_EIS'])
    x = XInput()
    deadline = time.monotonic() + 15
    try:
        while running:
            select.select([ei.fd, x.fd], [], [], 0.1)
            ei.dispatch()
            if not ei.devices and time.monotonic() > deadline:
                raise RuntimeError('Gamescope did not resume an input device')
            if ei.devices:
                (Path(os.environ['UURB_STEAMOS_ROOT']) / 'runtime/gamescope-input.ready').touch()
            for kind, detail in x.events():
                if kind == 17 or kind in (15, 16):
                    # Absolute synthetic warps do not unhide gamescope's cursor.
                    ei.send(1, 'ei_device_pointer_motion', 0.0, 0.0)
                    ei.send(2, 'ei_device_pointer_motion_absolute', *x.position())
                if kind in (13, 14):
                    key = detail - 8  # Xorg evdev keycodes have an eight-key offset.
                    if 0 <= key <= 767 and ei.send(4, 'ei_device_keyboard_key', key, kind == 13):
                        (ei.keys.add if kind == 13 else ei.keys.discard)(key)
                if kind in (15, 16):
                    if detail in (4, 5, 6, 7):
                        if kind == 15:
                            # EIS axis polarity differs from the KRDP path.
                            dx = {6: -120, 7: 120}.get(detail, 0)
                            dy = {4: -120, 5: 120}.get(detail, 0)
                            ei.send(16, 'ei_device_scroll_discrete', dx, dy)
                    else:
                        button = {1: 272, 2: 274, 3: 273, 8: 275, 9: 276}.get(detail)
                        if button and ei.send(32, 'ei_device_button_button', button, kind == 15):
                            (ei.buttons.add if kind == 15 else ei.buttons.discard)(button)
    finally:
        ei.close()


if __name__ == '__main__':
    main()
