#!/usr/bin/python3
"""Authenticated bitmap/file clipboard adapter. X11/XWayland selection owner."""
import argparse
import hashlib
import hmac
import io
import json
import os
from pathlib import Path
import queue
import select
import signal
import socket
import struct
import subprocess
import tempfile
import threading
import time

from PIL import Image
from Xlib import X, Xatom, display, protocol
from Xlib.ext import xfixes

MAGIC = 0x43425555
MAX_BYTES = 64 * 1024 * 1024
MAX_PIXELS = 16 * 1024 * 1024
TEXT, PNG, DIB, GET_IMAGE, FILE, GET_HOST = range(6)
Image.MAX_IMAGE_PIXELS = MAX_PIXELS


def png_image(data):
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("invalid PNG")
    width, height = struct.unpack_from(">II", data, 16)
    if width * height > MAX_PIXELS:
        raise ValueError("image too large")
    image = Image.open(io.BytesIO(data))
    if image.format != "PNG" or image.width * image.height > MAX_PIXELS:
        raise ValueError("unsupported image")
    return image.convert("RGBA")


def dib_image(data):
    if len(data) < 40:
        raise ValueError("short DIB")
    header, width, height, planes, bits, compression = struct.unpack_from("<IiiHHI", data)
    if header not in (40, 108, 124) or planes != 1 or width <= 0 or height == 0:
        raise ValueError("unsupported DIB header")
    if bits not in (24, 32) or compression not in (0, 3):
        raise ValueError("only uncompressed RGB24/BGRA32 supported")
    if width * abs(height) > MAX_PIXELS:
        raise ValueError("image too large")
    offset = header
    alpha = False
    if compression == 3:
        masks = struct.unpack_from("<III", data, 40)
        if masks != (0xFF0000, 0xFF00, 0xFF):
            raise ValueError("unsupported bitmap masks")
        if header == 40:
            offset += 12
        else:
            alpha = struct.unpack_from("<I", data, 52)[0] == 0xFF000000
    stride = ((width * bits + 31) // 32) * 4
    if offset + stride * abs(height) > len(data):
        raise ValueError("truncated pixels")
    image = Image.frombytes("RGBA" if bits == 32 else "RGB", (width, abs(height)),
                            data[offset:offset + stride * abs(height)],
                            "raw", "BGRA" if bits == 32 else "BGR",
                            stride, -1 if height > 0 else 1).convert("RGBA")
    if not alpha:
        image.putalpha(255)
    return image


def image_dib(image):
    header = bytearray(124)
    struct.pack_into("<IiiHHII", header, 0, 124, image.width, -image.height,
                     1, 32, 3, image.width * image.height * 4)
    struct.pack_into("<IIIII", header, 40, 0xFF0000, 0xFF00, 0xFF,
                     0xFF000000, 0x73524742)
    return bytes(header) + image.tobytes("raw", "BGRA")


def stage_file(packet, root):
    if len(packet) < 4:
        raise ValueError("short file packet")
    length, = struct.unpack_from("<I", packet)
    if not 0 < length <= 1024 or 4 + length > len(packet):
        raise ValueError("invalid filename")
    name = packet[4:4 + length].decode("utf-8")
    if name in (".", "..") or any(c in name for c in "/\\\0") or len(name.encode()) > 255:
        raise ValueError("invalid basename")
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    folder = Path(tempfile.mkdtemp(prefix="copy-", dir=root))
    path = folder / name
    try:
        with path.open("xb") as output:
            os.chmod(path, 0o600)
            output.write(packet[4 + length:])
            output.flush()
            os.fsync(output.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        folder.rmdir()
        raise
    return path


class Clipboard:
    def __init__(self, staging, status_file):
        self.d = display.Display()
        self.window = self.d.screen().root.create_window(
            0, 0, 1, 1, 0, X.CopyFromParent, X.InputOutput, X.CopyFromParent)
        self.clip = self.d.intern_atom("CLIPBOARD")
        self.targets = self.d.intern_atom("TARGETS")
        self.incr = self.d.intern_atom("INCR")
        self.values = {}
        self.transfers = {}
        self.staging = staging
        self.status_file = status_file
        self.image_digest = None
        self.text_digest = None
        self.image_dirty = False
        self.d.xfixes_query_version()
        self.d.xfixes_select_selection_input(self.window, self.clip, 7)
        self.d.flush()

    def record(self, data):
        self.status_file.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary = self.status_file.with_suffix(".tmp")
        temporary.write_text(json.dumps({"timestamp": time.time(), **data}) + "\n")
        temporary.replace(self.status_file)

    def publish(self, values, primary=False):
        atoms = {self.d.intern_atom(k): v for k, v in values.items()}
        self.values[self.clip] = atoms
        self.window.set_selection_owner(self.clip, X.CurrentTime)
        if primary:
            self.values[Xatom.PRIMARY] = atoms
            self.window.set_selection_owner(Xatom.PRIMARY, X.CurrentTime)
        self.d.sync()
        if self.d.get_selection_owner(self.clip) != self.window:
            raise RuntimeError("clipboard owner was not acquired")

    def operation(self, kind, data):
        if kind == TEXT:
            text = data.decode("utf-8")
            if "\0" in text or not text or len(data) > 4194304:
                raise ValueError("invalid text")
            self.publish({"UTF8_STRING": data, "text/plain;charset=utf-8": data}, True)
            self.image_digest = None
            self.text_digest = hashlib.sha256(data).digest()
            self.record({"kind": "text", "direction": "controller-to-native"})
        elif kind in (PNG, DIB):
            image = png_image(data) if kind == PNG else dib_image(data)
            output = io.BytesIO()
            image.save(output, format="PNG")
            self.image_digest = hashlib.sha256(image.tobytes()).digest()
            self.text_digest = None
            self.publish({"image/png": output.getvalue()})
            self.record({"kind": "image", "direction": "controller-to-native",
                         "width": image.width, "height": image.height,
                         "pixel_rgb_sha256": hashlib.sha256(image.convert("RGB").tobytes()).hexdigest()})
        elif kind == FILE:
            path = stage_file(data, self.staging)
            uri = path.as_uri().encode()
            self.publish({"text/uri-list": uri + b"\r\n",
                          "x-special/gnome-copied-files": b"copy\n" + uri + b"\n"})
            self.image_digest = None
            self.text_digest = None
            self.record({"kind": "file", "direction": "controller-to-native",
                         "staged_path": str(path), "size": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        elif kind in (GET_IMAGE, GET_HOST):
            if not self.image_dirty:
                return b""
            self.image_dirty = False
            if self.d.get_selection_owner(self.clip) == self.window:
                return b""
            try:
                targets = subprocess.run(["/usr/bin/xclip", "-selection", "clipboard",
                                          "-out", "-target", "TARGETS"],
                                         capture_output=True, timeout=1)
                offered = targets.stdout.decode(errors="replace").splitlines()
                target = next((name for name in ("image/png", "image/bmp")
                               if name in offered), None)
                if target is None and kind == GET_HOST:
                    target = next((name for name in ("UTF8_STRING", "text/plain;charset=utf-8")
                                   if name in offered), None)
                if target is None:
                    self.image_digest = self.text_digest = None
                    return b""
                result = subprocess.run(["/usr/bin/xclip", "-selection", "clipboard",
                                         "-out", "-target", target],
                                        capture_output=True, timeout=1)
                if result.returncode or len(result.stdout) > MAX_BYTES:
                    return b""
                if not target.startswith("image/"):
                    data = result.stdout
                    data.decode("utf-8")
                    if not data or b"\0" in data or len(data) > 4194304:
                        return b""
                    digest = hashlib.sha256(data).digest()
                    self.image_digest = None
                    if digest == self.text_digest:
                        return b""
                    self.text_digest = digest
                    self.record({"kind": "text", "direction": "native-to-wine-prepared"})
                    return struct.pack("<I", TEXT) + data
                if target == "image/png":
                    image = png_image(result.stdout)
                else:
                    image = Image.open(io.BytesIO(result.stdout))
                    if image.format != "BMP" or image.width * image.height > MAX_PIXELS:
                        raise ValueError("unsupported BMP")
                    image = image.convert("RGBA")
            except (ValueError, OSError, subprocess.TimeoutExpired, Image.DecompressionBombError):
                self.image_digest = None
                return b""
            digest = hashlib.sha256(image.tobytes()).digest()
            self.text_digest = None
            if digest == self.image_digest:
                return b""
            self.image_digest = digest
            self.record({"kind": "image", "direction": "native-to-wine-prepared",
                         "width": image.width, "height": image.height,
                         "pixel_rgb_sha256": hashlib.sha256(image.convert("RGB").tobytes()).hexdigest()})
            payload = image_dib(image)
            return struct.pack("<I", DIB) + payload if kind == GET_HOST else payload
        else:
            raise ValueError("unknown clipboard operation")
        return None

    def event(self, event):
        if isinstance(event, xfixes.SelectionNotify):
            if event.selection == self.clip and event.owner != self.window:
                self.image_dirty = True
        elif event.type == X.SelectionRequest:
            prop = event.property or event.target
            values = self.values.get(event.selection, {})
            if event.target == self.targets:
                event.requestor.change_property(prop, Xatom.ATOM, 32,
                                                [self.targets, *values])
            elif event.target in values:
                data = values[event.target]
                if len(data) > 65536:
                    event.requestor.change_attributes(event_mask=X.PropertyChangeMask)
                    event.requestor.change_property(prop, self.incr, 32, [len(data)])
                    self.transfers[(event.requestor.id, prop)] = (
                        event.requestor, event.target, data, 0, time.monotonic())
                else:
                    event.requestor.change_property(prop, event.target, 8, data)
            else:
                prop = X.NONE
            event.requestor.send_event(protocol.event.SelectionNotify(
                time=event.time, requestor=event.requestor, selection=event.selection,
                target=event.target, property=prop))
            self.d.flush()
        elif event.type == X.PropertyNotify and event.state == X.PropertyDelete:
            key = (event.window.id, event.atom)
            if key in self.transfers:
                window, target, data, offset, _ = self.transfers[key]
                chunk = data[offset:offset + 65536]
                window.change_property(event.atom, target, 8, chunk)
                if chunk:
                    self.transfers[key] = (window, target, data, offset + len(chunk),
                                           time.monotonic())
                else:
                    del self.transfers[key]
                self.d.flush()
        now = time.monotonic()
        self.transfers = {k: v for k, v in self.transfers.items() if now - v[4] < 10}


def exact(client, length):
    chunks = bytearray()
    while len(chunks) < length:
        chunk = client.recv(min(65536, length - len(chunks)))
        if not chunk:
            raise EOFError()
        chunks.extend(chunk)
    return bytes(chunks)


def serve(listener, token, work):
    while True:
        client, _ = listener.accept()
        with client:
            client.settimeout(2)
            try:
                magic, version = struct.unpack("<II", exact(client, 8))
                if magic != MAGIC or version != 1 or not hmac.compare_digest(exact(client, 64), token):
                    continue
                client.sendall(struct.pack("<IIII", MAGIC, 0, 1, 0))
                while True:
                    magic, sequence, length, kind = struct.unpack("<IIII", exact(client, 16))
                    if magic != MAGIC or length > MAX_BYTES or kind > GET_HOST:
                        raise ValueError("invalid request")
                    data = exact(client, length)
                    answer = queue.Queue(1)
                    work.put((kind, data, answer))
                    output, error = answer.get(timeout=3)
                    size = len(output) if kind in (GET_IMAGE, GET_HOST) else (length if not error else 0)
                    client.sendall(struct.pack("<IIII", MAGIC, sequence, size, error))
                    if kind in (GET_IMAGE, GET_HOST) and output:
                        client.sendall(output)
            except (EOFError, OSError, ValueError, queue.Empty):
                pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ready-file", type=Path, required=True)
    parser.add_argument("--staging", type=Path, default=Path.home() / ".local/share/uu-remote/clipboard-files")
    parser.add_argument("--status-file", type=Path, default=Path.home() / ".local/state/uu-remote-bridge/clipboard-status.json")
    args = parser.parse_args()
    token = os.environ["UURB_X11_CLIPBOARD_TOKEN"].encode()
    if len(token) != 64 or not all(c in b"0123456789abcdefABCDEF" for c in token):
        raise SystemExit("invalid clipboard token")
    os.umask(0o077)
    clipboard = Clipboard(args.staging, args.status_file)
    work = queue.Queue(8)
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    threading.Thread(target=serve, args=(listener, token, work), daemon=True).start()
    args.ready_file.write_text(str(listener.getsockname()[1]) + "\n")
    def stop(*_):
        raise SystemExit(0)
    signal.signal(signal.SIGTERM, stop)
    try:
        print("Native clipboard ready; text+bitmap+single-file; bitmap bidirectional.", flush=True)
        while True:
            while clipboard.d.pending_events():
                clipboard.event(clipboard.d.next_event())
            try:
                kind, data, answer = work.get_nowait()
            except queue.Empty:
                select.select([clipboard.d.fileno()], [], [], 0.02)
                continue
            try:
                output = clipboard.operation(kind, data)
                answer.put((output or b"", 0))
            except (ValueError, OSError, RuntimeError, struct.error):
                answer.put((b"", 0x3001))
    finally:
        args.ready_file.unlink(missing_ok=True)
        listener.close()
        clipboard.d.close()


if __name__ == "__main__":
    main()
