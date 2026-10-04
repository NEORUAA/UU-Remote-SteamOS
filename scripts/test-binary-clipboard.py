#!/usr/bin/python3
"""One small bidirectional bitmap and HDROP/OLE probe; isolated X/Wine only."""
import hashlib
import io
import json
import os
from pathlib import Path
import secrets
import socket
import struct
import subprocess
import tempfile
import time

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
WINE = "/opt/wine-stable/bin/wine"
MAGIC = 0x43425555


def wait_for(check, seconds=12):
    deadline = time.monotonic() + seconds
    while not check():
        if time.monotonic() > deadline:
            raise AssertionError("isolated clipboard operation timed out")
        time.sleep(0.05)


def exact(client, length):
    data = bytearray()
    while len(data) < length:
        chunk = client.recv(length - len(data))
        assert chunk
        data.extend(chunk)
    return bytes(data)


def main():
    with tempfile.TemporaryDirectory(prefix="uurb-binary-clip-") as temporary:
        lab = Path(temporary)
        processes = []
        logs = []
        base_env = dict(os.environ, WINEPREFIX=str(lab / "wine"), WINEDEBUG="-all",
                        WINEDLLOVERRIDES="mscoree,mshtml=")
        def launch(argv, env):
            log = open(lab / ("log-" + str(len(logs))), "wb")
            logs.append(log)
            proc = subprocess.Popen(argv, env=env, stdout=log, stderr=log)
            processes.append(proc)
            return proc
        def seed(data, target):
            proc = subprocess.Popen(["xclip", "-selection", "clipboard", "-in",
                                     "-target", target, "-verbose", "-loops", "0"],
                                    env=host, stdin=subprocess.PIPE,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            processes.append(proc)
            proc.stdin.write(data)
            proc.stdin.close()
            time.sleep(0.15)
        try:
            displays = []
            for _ in range(2):
                proc = subprocess.Popen(["Xvfb", "-displayfd", "1", "-screen", "0",
                                         "800x600x24", "-ac", "-nolisten", "tcp"],
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                processes.append(proc)
                displays.append(":" + proc.stdout.readline().decode().strip())
            host = dict(base_env, DISPLAY=displays[0])
            windows = dict(base_env, DISPLAY=displays[1])
            companion = lab / "companion.exe"
            fixture = lab / "GameViewer.exe"
            subprocess.run(["x86_64-w64-mingw32-gcc", "-std=c11", "-O2", "-Wall",
                            "-Wextra", "-Werror", "-municode", "-I", str(ROOT / "src"),
                            "-o", str(companion), str(ROOT / "src/uu_wine_clipboard_bridge.c"),
                            "-lws2_32"], check=True)
            subprocess.run(["x86_64-w64-mingw32-gcc", "-std=c11", "-O2", "-Wall",
                            "-Wextra", "-Werror", "-municode", "-o", str(fixture),
                            str(ROOT / "tests/probes/uu_binary_clipboard_fixture.c"),
                            "-lole32", "-luuid", "-lshell32", "-lgdi32"], check=True)
            subprocess.run(["/opt/wine-stable/bin/wineboot", "-u"], env=windows,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=40, check=True)
            token = secrets.token_hex(32)
            ready = lab / "port"
            status = lab / "status.json"
            launch(["/usr/bin/python3", str(ROOT / "scripts/uu-clipboard-native.py"),
                    "--ready-file", str(ready), "--staging", str(lab / "staging"),
                    "--status-file", str(status)],
                   dict(host, UURB_X11_CLIPBOARD_TOKEN=token, UURB_CLIPBOARD_PROGRESS="0"))
            wait_for(ready.exists)
            adapter = launch([WINE, str(companion)], dict(windows,
                UURB_X11_CLIPBOARD_PORT=ready.read_text().strip(),
                UURB_X11_CLIPBOARD_TOKEN=token, UURB_CLIPBOARD_EXTENDED="1"))
            time.sleep(0.5)
            def state():
                return json.loads(status.read_text()) if status.exists() else {}
            launch([WINE, str(fixture), "dib"], windows)
            wait_for(lambda: state().get("width") == 3)
            received = subprocess.check_output(
                ["xclip", "-selection", "clipboard", "-out", "-target", "image/png"],
                env=host, timeout=5)
            expected = [(255,0,0,255), (0,255,0,128), (0,0,255,255),
                        (255,255,255,0), (10,20,30,255), (0,0,0,255)]
            assert Image.open(io.BytesIO(received)).convert("RGBA").tobytes() == bytes(
                component for pixel in expected for component in pixel)
            previous_at = state()["timestamp"]
            launch([WINE, str(fixture), "dib-stale-v5"], windows)
            wait_for(lambda: state().get("timestamp", 0) > previous_at)
            received = subprocess.check_output(
                ["xclip", "-selection", "clipboard", "-out", "-target", "image/png"],
                env=host, timeout=5)
            assert Image.open(io.BytesIO(received)).convert("RGB").tobytes() == bytes(
                component for pixel in expected for component in pixel[:3])
            outgoing = Image.new("RGBA", (55, 39))
            outgoing.putdata([((x * 23 + y * 7 + 102) % 256,
                               (x * 11 + y * 31 + 72) % 256,
                               (x * 3 + y * 17 + 118) % 256,
                               (x * 19 + y * 13) % 256)
                              for y in range(39) for x in range(55)])
            encoded = io.BytesIO()
            outgoing.save(encoded, format="PNG")
            seed(encoded.getvalue(), "image/png")
            wait_for(lambda: state().get("direction") == "native-to-wine-prepared")
            dump = lab / "reverse.dib"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-image",
                        "Z:" + str(dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            raw = dump.read_bytes()
            assert struct.unpack_from("<ii", raw, 4) == (55, -39)
            assert raw[124:] == outgoing.tobytes("raw", "BGRA")
            png_dump = lab / "reverse.png"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-png",
                        "Z:" + str(png_dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            assert png_dump.read_bytes() == encoded.getvalue(), "PNG source bytes changed"
            assert Image.open(png_dump).convert("RGBA").tobytes() == outgoing.tobytes()
            dib_dump = lab / "reverse-ole.dib"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-dib-ole",
                        "Z:" + str(dib_dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            raw = dib_dump.read_bytes()
            assert struct.unpack_from("<ii", raw, 4) == (55, -39)
            assert struct.unpack_from("<H", raw, 14)[0] == 24
            bgr = outgoing.convert("RGB").tobytes("raw", "BGR")
            assert raw[40:] == b"".join(bgr[y * 165:(y + 1) * 165] + b"\0" * 3
                                       for y in range(39))
            assert Image.open(io.BytesIO(raw)).convert("RGB").tobytes() == outgoing.convert("RGB").tobytes()
            gdi_dump = lab / "reverse-gdi.bgrx"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-dib-gdi",
                        "Z:" + str(gdi_dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            assert Image.frombytes("RGB", (55, 39), gdi_dump.read_bytes(),
                                   "raw", "BGRX").tobytes() == outgoing.convert("RGB").tobytes()
            native_text = "Ubuntu 中文\nsecond line"
            seed(native_text.encode(), "UTF8_STRING")
            wait_for(lambda: state().get("kind") == "text" and
                     state().get("direction") == "native-to-wine-prepared")
            text_dump = lab / "reverse-text.bin"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-text",
                        "Z:" + str(text_dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            assert text_dump.read_bytes().decode("utf-16-le").rstrip("\0") == native_text
            launch([WINE, str(fixture), "text"], windows)
            wait_for(lambda: state().get("direction") == "controller-to-native" and
                     state().get("kind") == "text")
            text = subprocess.check_output(["xclip", "-selection", "clipboard", "-out",
                                           "-target", "UTF8_STRING"], env=host, timeout=5)
            assert text.decode() == "Windows 中文\nsecond line"
            source = lab / "中文 file.bin"
            content = b"single-file\0\xff\n"
            source.write_bytes(content)
            launch([WINE, str(fixture), "drop", "Z:" + str(source)], windows)
            wait_for(lambda: state().get("kind") == "file")
            first = Path(state()["staged_path"])
            assert first.read_bytes() == content
            uris = subprocess.check_output(
                ["xclip", "-selection", "clipboard", "-out", "-target", "text/uri-list"],
                env=host, timeout=5).decode().strip()
            assert uris == first.as_uri()
            launch([WINE, str(fixture), "virtual"], windows)
            wait_for(lambda: state().get("staged_path", "").endswith("virtual.txt"))
            assert Path(state()["staged_path"]).read_bytes() == b"virtual-file\0\xff\n"
            second = lab / "second.bin"
            second.write_bytes(b"multi-file-data\0\xff" * 8192)
            previous_at = state()["timestamp"]
            launch([WINE, str(fixture), "drop", "Z:" + str(source), "Z:" + str(second)], windows)
            wait_for(lambda: state().get("timestamp", 0) > previous_at and state().get("file_count") == 2)
            assert [Path(p).read_bytes() for p in state()["staged_paths"]] == [content, second.read_bytes()]
            uris = subprocess.check_output(["xclip", "-selection", "clipboard", "-out", "-target",
                                            "text/uri-list"], env=host, timeout=5).decode().splitlines()
            assert uris == [Path(p).as_uri() for p in state()["staged_paths"]]
            previous_at = state()["timestamp"]
            launch([WINE, str(fixture), "virtual-multiple"], windows)
            wait_for(lambda: state().get("timestamp", 0) > previous_at and
                     state().get("files", [{}])[-1].get("name") == "unknown-size.txt")
            assert [Path(p).read_bytes() for p in state()["staged_paths"]] == [b"virtual-file\0\xff\n"] * 2
            adapter.terminate()
            adapter.wait(timeout=5)
            client = socket.create_connection(("127.0.0.1", int(ready.read_text())), timeout=5)
            client.sendall(struct.pack("<II", MAGIC, 1) + token.encode())
            assert struct.unpack("<IIII", exact(client, 16))[2:] == (1, 0)
            def request(kind, payload=b""):
                client.sendall(struct.pack("<IIII", MAGIC, 99, len(payload), kind) + payload)
                _, _, length, error = struct.unpack("<IIII", exact(client, 16))
                return exact(client, length) if kind in (3, 5) and length else (length, error)
            seed(encoded.getvalue(), "image/png")
            assert isinstance(request(3), bytes)
            seed(b"foreign text", "UTF8_STRING")
            assert request(3) == (0, 0)
            seed(encoded.getvalue(), "image/png")
            assert isinstance(request(3), bytes), "same-image-after-text was suppressed"
            opaque = outgoing.convert("RGB")
            for format_name, target in (("PNG", "image/png"), ("BMP", "image/bmp")):
                encoded_opaque = io.BytesIO()
                opaque.save(encoded_opaque, format=format_name)
                seed(encoded_opaque.getvalue(), target)
                response = request(5)
                if format_name == "PNG":
                    assert isinstance(response, bytes) and response[:4] == struct.pack("<I", 2)
                else:
                    assert response == (0, 0), "same pixels returned in another format were echoed"
            seed(b"new native text", "UTF8_STRING")
            assert request(5) == struct.pack("<I", 0) + b"new native text"
            assert request(5) == (0, 0), "unchanged clipboard was replayed"
            invalid = struct.pack("<I", 4) + b"../x" + b"data"
            assert request(4, invalid)[1] != 0
            packet = struct.pack("<I", 8) + b"same.bin" + b"first"
            assert request(4, packet) == (len(packet), 0)
            previous = Path(state()["staged_path"])
            packet = struct.pack("<I", 8) + b"same.bin" + b"second"
            assert request(4, packet) == (len(packet), 0)
            assert Path(state()["staged_path"]) != previous and previous.read_bytes() == b"first"
            count = len(list((lab / "staging").glob("*")))
            client.sendall(struct.pack("<IIII", MAGIC, 100, 100, 4) + b"short")
            client.close()
            time.sleep(0.15)
            assert len(list((lab / "staging").glob("*"))) == count
            client = socket.create_connection(("127.0.0.1", int(ready.read_text())), timeout=5)
            client.sendall(struct.pack("<II", MAGIC, 1) + token.encode())
            assert struct.unpack("<IIII", exact(client, 16))[2:] == (1, 0)
            progress = lab / "clipboard-transfer.json"
            def manifest(entries):
                return struct.pack("<I", len(entries)) + b"".join(
                    struct.pack("<Iq", len(name.encode()), size) + name.encode() for name, size in entries)
            chunk = b"real bytes" * 4096
            begin = manifest([("same.bin", len(chunk) * 2), ("same.bin", -1)])
            assert request(6, begin) == (len(begin), 0)
            old_uris = subprocess.check_output(["xclip", "-selection", "clipboard", "-out", "-target",
                                               "text/uri-list"], env=host, timeout=5)
            time.sleep(0.12)
            assert request(7, struct.pack("<I", 0) + chunk)[1] == 0
            p = json.loads(progress.read_text())
            assert p["received"] == p["bytes_received"] == len(chunk) and p["percent"] == 50
            assert p["bytes_total"] is None and p["total_percent"] is None
            assert subprocess.check_output(["xclip", "-selection", "clipboard", "-out", "-target",
                                            "text/uri-list"], env=host, timeout=5) == old_uris
            assert request(7, struct.pack("<I", 0) + chunk)[1] == 0
            assert request(8, struct.pack("<I", 0))[1] == 0
            p = json.loads(progress.read_text())
            assert p["file_index"] == 2 and p["file_count"] == 2 and p["total"] is None
            assert request(7, struct.pack("<I", 1) + b"done")[1] == 0
            assert request(8, struct.pack("<I", 1))[1] == 0
            p = json.loads(progress.read_text())
            assert p["state"] == "completed" and p["bytes_received"] == p["bytes_total"] == len(chunk) * 2 + 4
            paths = [Path(p) for p in state()["staged_paths"]]
            assert paths[0].read_bytes() == chunk * 2 and paths[1].read_bytes() == b"done"
            assert paths[0].name == "same.bin" and paths[1].name == "same (2).bin"
            before = set((lab / "staging").iterdir())
            begin = manifest([("partial.bin", 100)])
            assert request(6, begin)[1] == 0
            assert request(7, struct.pack("<I", 0) + b"short")[1] == 0
            client.close()
            wait_for(lambda: json.loads(progress.read_text()).get("state") == "failed")
            assert set((lab / "staging").iterdir()) == before
            client = socket.create_connection(("127.0.0.1", int(ready.read_text())), timeout=5)
            client.sendall(struct.pack("<II", MAGIC, 1) + token.encode())
            assert struct.unpack("<IIII", exact(client, 16))[2:] == (1, 0)
            assert request(6, manifest([("large.bin", 64 * 1024 * 1024 + 1)]))[1] != 0
            assert json.loads(progress.read_text())["state"] == "failed"
            print(json.dumps({"bitmap_wine_to_native_pixels": "PASS",
                              "bitmap_native_to_wine_different_pixels": "PASS",
                              "text_unicode_multiline_each_direction": "PASS",
                              "same_pixels_PNG_BMP_echo_suppressed": "PASS",
                              "native_text_not_replayed": "PASS",
                              "primary_DIB_over_stale_synthesized_V5": "PASS",
                              "original_PNG_OLE_HGLOBAL_bytes_and_RGBA": "PASS",
                              "PNG_first_enumeration_and_DIB_OLE_preserved": "PASS",
                              "single_file_HDROP": "PASS", "virtual_OLE_IStream": "PASS",
                              "URI_list_published": "PASS", "same_image_after_external_text": "PASS",
                              "path_traversal_rejected": "PASS", "duplicate_name_no_overwrite": "PASS",
                              "partial_transfer_no_publish": "PASS",
                              "multiple_HDROP_and_OLE_files_exact_bytes": "PASS",
                              "multiple_file_URI_publication_after_completion": "PASS",
                              "real_byte_counters_and_unknown_total": "PASS",
                              "duplicate_names_within_batch_no_overwrite": "PASS",
                              "stream_disconnect_cleanup_and_failure_state": "PASS",
                              "file_size_limit_failure_visible": "PASS",
                              "file_sha256": hashlib.sha256(content).hexdigest(),
                              "real_controller_tested": False}, indent=2))
        except BaseException:
            for log in logs:
                log.flush()
            for log in sorted(lab.glob("log-*")):
                print(log.name, log.read_text(errors="replace")[-1600:])
            if (lab / "status.json").exists():
                print("last-native-status", (lab / "status.json").read_text())
            raise
        finally:
            for proc in reversed(processes):
                if proc.poll() is None:
                    proc.terminate()
            subprocess.run(["/opt/wine-stable/bin/wineserver", "-k"], env=base_env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for proc in processes:
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
            for log in logs:
                log.close()


if __name__ == "__main__":
    main()
