#!/usr/bin/env python3
"""Short native transport probe; owns only a temporary helper and tmux socket."""
import json
import os
from pathlib import Path
import pwd
import re
import secrets
import shlex
import socket
import struct
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
TMUX = "/usr/bin/tmux"


class Broker:
    def __init__(self, binary, directory, mode=None):
        self.ready = directory / "terminal.port"
        self.tmux_socket = directory / "terminal-tmux.sock"
        env = os.environ.copy()
        env["UURB_TERMINAL_BRIDGE_TOKEN"] = secrets.token_hex(32)
        env["UURB_TERMINAL_BRIDGE_PORT"] = "12345"
        env.pop("UURB_TERMINAL_SESSION_MODE", None)
        if mode is not None:
            env["UURB_TERMINAL_SESSION_MODE"] = mode
        self.token = env["UURB_TERMINAL_BRIDGE_TOKEN"].encode()
        self.log = open(directory / "broker.log", "wb")
        self.process = subprocess.Popen(
            [str(binary), "--ready-file", str(self.ready)],
            env=env, stdout=self.log, stderr=self.log)
        self.clients = []
        try:
            deadline = time.monotonic() + 5
            while not self.ready.exists():
                if self.process.poll() is not None or time.monotonic() > deadline:
                    raise AssertionError("isolated broker did not become ready")
                time.sleep(0.02)
            self.port = int(self.ready.read_text())
        except BaseException:
            self.close()
            raise

    def connect(self):
        client = socket.create_connection(("127.0.0.1", self.port), timeout=5)
        self.clients.append(client)
        client.sendall(struct.pack("!IHHHH", 0x55555242, 1, 64, 96, 28) + self.token)
        assert client.recv(1) == b"\x06", "handshake was not accepted"
        return client

    def tmux(self, *args):
        return subprocess.check_output(
            [TMUX, "-S", str(self.tmux_socket), *args], timeout=5)

    def close(self):
        for client in self.clients:
            client.close()
        self.process.terminate()
        self.process.wait(timeout=5)
        self.log.close()
        if self.tmux_socket.exists():
            subprocess.run([TMUX, "-S", str(self.tmux_socket), "kill-server"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=5, check=True)


def send(client, command):
    data = command.encode() + b"\r"
    client.sendall(struct.pack("!B3xI", 1, len(data)) + data)


def receive(client, pattern):
    data = b""
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        match = re.search(pattern, data)
        if match:
            return match
        client.settimeout(max(0.01, deadline - time.monotonic()))
        chunk = client.recv(65536)
        assert chunk, "terminal closed before the expected marker"
        data += chunk
    raise AssertionError("terminal marker timed out")


def until(check):
    deadline = time.monotonic() + 5
    while not check():
        assert time.monotonic() < deadline, "state did not settle"
        time.sleep(0.02)


def probe():
    assert os.access(TMUX, os.X_OK), "this opt-in probe requires installed /usr/bin/tmux"
    with tempfile.TemporaryDirectory(prefix="uurb-pty-test-") as temporary:
        base = Path(temporary)
        binary = base / "uu-terminal-bridge"
        subprocess.run(["gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                        "-I", str(ROOT / "src"), "-o", str(binary),
                        str(ROOT / "src/uu_terminal_bridge.c"), "-lutil"], check=True)
        persistent = base / "persistent"
        persistent.mkdir()
        work = base / "work"
        work.mkdir()
        broker = Broker(binary, persistent, "persistent")
        try:
            first = broker.connect()
            send(first, "printf 'READY%s\\n' '-MARKER'")
            receive(first, rb"READY-MARKER")
            account = pwd.getpwuid(os.getuid())
            assert broker.tmux("display-message", "-p", "-t", "main:0.0",
                               "#{pane_current_path}").decode().strip() == account.pw_dir
            assert broker.tmux("show-options", "-gv", "default-shell").decode().strip() == account.pw_shell
            send(first, "cd " + shlex.quote(str(work)) +
                 "; sleep 40 & bg=$!; printf 'STATE%s %s %s\\n' '-MARKER' \"$$\" \"$bg\"")
            initial = receive(first, rb"STATE-MARKER (\d+) (\d+)")
            shell_pid, background_pid = map(int, initial.groups())
            assert broker.tmux("display-message", "-p", "-t", "main:0.0",
                               "#{pane_pid}").strip() == str(shell_pid).encode()
            first.close()
            until(lambda: not broker.tmux("list-clients", "-F", "#{client_pid}").strip())
            os.kill(background_pid, 0)
            second = broker.connect()
            send(second, "printf 'AGAIN%s %s\\n' '-MARKER' \"$$\"")
            resumed = int(receive(second, rb"AGAIN-MARKER (\d+)").group(1))
            assert resumed == shell_pid, "reconnect created a different shell"
            assert broker.tmux("display-message", "-p", "-t", "main:0.0",
                               "#{pane_current_path}").decode().strip() == str(work)
            os.kill(background_pid, 0)
            send(second, "if printenv UURB_TERMINAL_BRIDGE_TOKEN UURB_TERMINAL_BRIDGE_PORT"
                 " >/dev/null; then printf 'BAD%s\\n' '-ENV'; else printf 'SAFE%s\\n' '-ENV'; fi")
            receive(second, rb"SAFE-ENV")
            server_env = broker.tmux("show-environment", "-g")
            assert b"UURB_TERMINAL_BRIDGE_TOKEN=" not in server_env
            assert b"UURB_TERMINAL_BRIDGE_PORT=" not in server_env
            second.sendall(struct.pack("!B3xIHH", 2, 4, 111, 33))
            until(lambda: broker.tmux("display-message", "-p", "-t", "main:0.0",
                                     "#{pane_width}x#{pane_height}").strip() == b"111x32")
            send(second, "printf 'SIZE%s ' '-MARKER'; stty size")
            receive(second, rb"SIZE-MARKER 32 111")
            second.sendall(struct.pack("!B3xI", 3, 0))
            second.settimeout(5)
            while second.recv(65536):
                pass
            third = broker.connect()
            send(third, "printf 'EOF%s %s\\n' '-RESUMED' \"$$\"")
            assert int(receive(third, rb"EOF-RESUMED (\d+)").group(1)) == shell_pid
            os.kill(background_pid, 0)
            result = {"persistent_reconnect": "PASS", "same_shell_PID": shell_pid,
                      "transport_EOF_detaches_without_ending_workspace": True,
                      "same_working_directory": True, "background_job_survived": True,
                      "transport_credentials_absent_in_shell_and_tmux": True,
                      "resize_outer": "111x33", "resize_pane": "111x32 (tmux status row)"}
        finally:
            broker.close()
        fresh_dir = base / "fresh"
        fresh_dir.mkdir()
        broker = Broker(binary, fresh_dir)
        try:
            client = broker.connect()
            send(client, "printf 'FRESH%s %s\\n' '-PID' \"$$\"")
            fresh_pid = int(receive(client, rb"FRESH-PID (\d+)").group(1))
            send(client, "exit")
            client.settimeout(5)
            while client.recv(65536):
                pass
            assert not broker.tmux_socket.exists(), "default fresh mode started tmux"
            result["default_fresh_exit"] = "PASS"
            result["fresh_shell_PID"] = fresh_pid
        finally:
            broker.close()
        result["owned_lab_resources_cleaned"] = True
        result["UU_controller_tested"] = False
        result["tmux_missing_fallback_tested"] = False
        return result


if __name__ == "__main__":
    print(json.dumps(probe(), ensure_ascii=False, indent=2))
