#!/usr/bin/python3
"""One isolated regression: a native copy must cancel an unfinished file batch."""
import json
import os
from pathlib import Path
import secrets
import socket
import struct
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
MAGIC = 0x43425555

def wait_for(check):
    deadline = time.monotonic() + 8
    while not check():
        if time.monotonic() >= deadline:
            raise AssertionError('native clipboard cancellation timed out')
        time.sleep(.02)

def exact(client, size):
    data = bytearray()
    while len(data) < size:
        chunk = client.recv(size - len(data))
        assert chunk
        data.extend(chunk)
    return bytes(data)

def main():
    with tempfile.TemporaryDirectory(prefix='uurb-file-cancel-') as temporary:
        lab = Path(temporary)
        processes = []
        try:
            server = subprocess.Popen(['Xvfb','-displayfd','1','-screen','0','800x600x24',
                                       '-ac','-nolisten','tcp'],stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL)
            processes.append(server)
            env = {**os.environ,'DISPLAY':':' + server.stdout.readline().decode().strip()}
            token = secrets.token_hex(32)
            ready, status, staging = lab/'port', lab/'status.json', lab/'staging'
            with (lab/'helper.log').open('wb') as log:
                helper = subprocess.Popen(['/usr/bin/python3',str(ROOT/'scripts/uu-clipboard-native.py'),
                    '--ready-file',str(ready),'--status-file',str(status),'--staging',str(staging)],
                    env={**env,'UURB_X11_CLIPBOARD_TOKEN':token,'UURB_CLIPBOARD_PROGRESS':'0'},
                    stdout=log,stderr=log)
                processes.append(helper)
            wait_for(ready.exists)
            client = socket.create_connection(('127.0.0.1',int(ready.read_text())),timeout=5)
            client.sendall(struct.pack('<II',MAGIC,1)+token.encode())
            assert struct.unpack('<IIII',exact(client,16))[2:] == (1,0)
            def request(kind,data=b''):
                client.sendall(struct.pack('<IIII',MAGIC,31,len(data),kind)+data)
                _,_,size,error = struct.unpack('<IIII',exact(client,16))
                return exact(client,size) if kind == 5 and size and not error else (size,error)
            name = b'cancelled.bin'
            begin = struct.pack('<I',1)+struct.pack('<Iq',len(name),100)+name
            assert request(6,begin) == (len(begin),0)
            progress = lab/'clipboard-transfer.json'
            assert json.loads(progress.read_text())['state'] == 'receiving'
            assert request(7,struct.pack('<I',0)+b'partial bytes')[1] == 0
            assert len(list(staging.glob('copy-*'))) == 1
            text = b'A new native copy takes priority'
            owner = subprocess.Popen(['xclip','-selection','clipboard','-in','-target','UTF8_STRING',
                                      '-verbose','-loops','0'],env=env,stdin=subprocess.PIPE,
                                     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            processes.append(owner)
            owner.stdin.write(text);owner.stdin.close()
            wait_for(lambda: json.loads(progress.read_text()).get('state') == 'failed')
            failure = json.loads(progress.read_text())
            assert 'new native clipboard' in failure['error']
            assert list(staging.glob('copy-*')) == []
            assert request(8,struct.pack('<I',0))[1] != 0
            actual = subprocess.check_output(['xclip','-selection','clipboard','-out','-target',
                                               'UTF8_STRING'],env=env,timeout=5)
            assert actual == text
            uri = subprocess.run(['xclip','-selection','clipboard','-out','-target','text/uri-list'],
                                 env=env,capture_output=True,timeout=5)
            assert b"file:" not in uri.stdout, "old file URI was published over the native text"
            assert request(5) == struct.pack('<I',0)+text
            client.close()
            print(json.dumps({'native_copy_during_file_transfer_cancels_old_batch':'PASS',
                              'first_begin_state':'receiving','partial_files_removed':True,
                              'stale_END_rejected':True,'native_text_preserved':True,
                              'old_file_URI_not_published':True,'new_native_text_forwardable':True,
                              'production_clipboard_touched':False,'keyboard_mouse_events_sent':False},indent=2))
        except BaseException:
            if (lab/'helper.log').exists():
                print((lab/'helper.log').read_text(errors='replace')[-1500:])
            raise
        finally:
            for proc in reversed(processes):
                if proc.poll() is None:
                    proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill();proc.wait()

if __name__ == '__main__':
    main()
