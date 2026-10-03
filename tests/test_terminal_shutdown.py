"""Exercise stalled clients against a private helper, never the installed bridge."""
import os
from pathlib import Path
import re
import signal
import socket
import struct
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TerminalShutdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory()
        cls.path = Path(cls.build.name)
        source = Path(os.environ.get("UURB_TERMINAL_TEST_SOURCE", ROOT / "src/uu_terminal_bridge.c")).read_text()
        # Retain real PTY/session teardown without executing the user's login profile.
        source = re.sub(r"static void run_login_shell\(void\)\n\{.*?\n\}",
                        "static void run_login_shell(void)\n{\n"
                        "    if (getenv(\"UURB_TEST_OUTPUT_FLOOD\")) {\n"
                        "        unsigned char output[8192];\n"
                        "        memset(output, 'X', sizeof(output));\n"
                        "        for (;;) if (write(1, output, sizeof(output)) < 0 && errno != EINTR) _exit(0);\n"
                        "    }\n    for (;;) pause();\n}", source, count=1, flags=re.S)
        (cls.path / "helper.c").write_text(source)
        subprocess.run(["gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT / "src"),
                        str(cls.path / "helper.c"), "-lutil", "-o", str(cls.path / "helper")], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.build.cleanup()

    def exercise_client(self, stage, stubborn=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ready = root / "ready"
            log_path = root / "log"
            with log_path.open("w") as log:
                process = subprocess.Popen([str(self.path / "helper"), "--ready-file", str(ready)],
                                           env={**os.environ, "UURB_TERMINAL_BRIDGE_TOKEN": "a" * 64,
                                                **({"UURB_TEST_OUTPUT_FLOOD": "1"} if stage == "socket-write" else {})},
                                           stdout=log, stderr=log, start_new_session=True)
                connection = None
                shell_pid = None
                try:
                    deadline = time.monotonic() + 3
                    while not ready.exists() and time.monotonic() < deadline:
                        self.assertIsNone(process.poll(), log_path.read_text())
                        time.sleep(0.01)
                    self.assertTrue(ready.exists(), log_path.read_text())
                    connection = socket.create_connection(("127.0.0.1", int(ready.read_text())), timeout=1)
                    if stage == "handshake":
                        connection.sendall(b"UU")
                    else:
                        connection.sendall(struct.pack("!IHHHH", 0x55555242, 1, 64, 80, 24) + b"a" * 64)
                        self.assertEqual(connection.recv(1), b"\x06")
                        deadline = time.monotonic() + 2
                        while time.monotonic() < deadline:
                            match = re.search(r"session opened pid=(\d+)", log_path.read_text())
                            if match:
                                shell_pid = int(match[1])
                                break
                            time.sleep(0.01)
                        self.assertIsNotNone(shell_pid)
                        if stage == "pty-write":
                            payload = b"x\n" * 32768
                            connection.sendall(struct.pack("!B3xI", 1, len(payload)) + payload)
                        elif stage == "socket-write":
                            connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
                            # Consume no output so the helper's nonblocking send fills.
                            time.sleep(0.5)
                        elif stage == "header":
                            connection.sendall(b"\x01\0")
                        else:
                            connection.sendall(struct.pack("!B3xI", 1, 4096) + b"x")
                    time.sleep(0.1)
                    if stubborn:
                        # Stop just this helper's handler to exercise bounded escalation.
                        children_file = Path(f"/proc/{process.pid}/task/{process.pid}/children")
                        children = [int(value) for value in children_file.read_text().split()]
                        self.assertEqual(len(children), 1)
                        os.kill(children[0], signal.SIGSTOP)
                    started = time.monotonic()
                    process.terminate()
                    process.wait(timeout=4)
                    self.assertLess(time.monotonic() - started, 3.5)
                    self.assertEqual(process.returncode, 0, log_path.read_text())
                    self.assertFalse(ready.exists())
                finally:
                    if connection:
                        connection.close()
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=2)
                    if shell_pid:
                        try:
                            os.killpg(shell_pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass

    def test_shutdown_interrupts_partial_handshake(self):
        self.exercise_client("handshake")

    def test_shutdown_interrupts_authenticated_partial_frame_header(self):
        self.exercise_client("header")

    def test_shutdown_interrupts_authenticated_partial_frame_body(self):
        self.exercise_client("body")

    def test_shutdown_escalates_only_owned_unresponsive_handler(self):
        self.exercise_client("body", stubborn=True)

    def test_shutdown_interrupts_pty_input_backpressure(self):
        self.exercise_client("pty-write")

    def test_shutdown_interrupts_client_output_backpressure(self):
        self.exercise_client("socket-write")


if __name__ == "__main__":
    unittest.main()
