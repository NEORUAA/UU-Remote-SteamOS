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
                            "-lole32", "-luuid", "-lshell32"], check=True)
            subprocess.run(["/opt/wine-stable/bin/wineboot", "-u"], env=windows,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=40, check=True)
            token = secrets.token_hex(32)
            ready = lab / "port"
            status = lab / "status.json"
            launch(["/usr/bin/python3", str(ROOT / "scripts/uu-clipboard-native.py"),
                    "--ready-file", str(ready), "--staging", str(lab / "staging"),
                    "--status-file", str(status)],
                   dict(host, UURB_X11_CLIPBOARD_TOKEN=token))
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
            outgoing = Image.new("RGBA", (2, 1))
            outgoing.putdata([(7,8,9,255), (40,50,60,100)])
            encoded = io.BytesIO()
            outgoing.save(encoded, format="PNG")
            seed(encoded.getvalue(), "image/png")
            wait_for(lambda: state().get("direction") == "native-to-wine-prepared")
            dump = lab / "reverse.dib"
            wait_for(lambda: subprocess.run([WINE, str(fixture), "read-image",
                        "Z:" + str(dump)], env=windows, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, timeout=5).returncode == 0)
            raw = dump.read_bytes()
            assert struct.unpack_from("<ii", raw, 4) == (2, -1)
            assert raw[124:132] == bytes([9,8,7,255,60,50,40,100])
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
            print(json.dumps({"bitmap_wine_to_native_pixels": "PASS",
                              "bitmap_native_to_wine_different_pixels": "PASS",
                              "text_unicode_multiline_each_direction": "PASS",
                              "same_pixels_PNG_BMP_echo_suppressed": "PASS",
                              "native_text_not_replayed": "PASS",
                              "primary_DIB_over_stale_synthesized_V5": "PASS",
                              "single_file_HDROP": "PASS", "virtual_OLE_IStream": "PASS",
                              "URI_list_published": "PASS", "same_image_after_external_text": "PASS",
                              "path_traversal_rejected": "PASS", "duplicate_name_no_overwrite": "PASS",
                              "partial_transfer_no_publish": "PASS",
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
