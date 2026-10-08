"""Guard private video patches and their PE exception metadata."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('video', ROOT / 'scripts/uu_steamos_video.py')
video = importlib.util.module_from_spec(spec)
spec.loader.exec_module(video)


def fixture():
    data = bytearray(1024)
    data[:2] = b'MZ'
    data[64:80] = b'Wine builtin DLL'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x8664, 1, 0, 0, 0, 240, 0x22)
    optional = 152
    struct.pack_into('<H', data, optional, 0x20b)
    struct.pack_into('<II', data, optional + 32, 4096, 512)
    struct.pack_into('<II', data, optional + 56, 8192, 512)
    struct.pack_into('<I', data, optional + 108, 16)
    struct.pack_into('<II', data, optional + 136, 0x1100, 36)
    data[392:400] = b'.text\0\0\0'
    struct.pack_into('<4I', data, 400, 512, 4096, 512, 512)
    struct.pack_into('<I', data, 428, 0x60000020)
    patches = []
    for index, rva in enumerate((0x1010, 0x1030, 0x1050)):
        offset = 512 + rva - 4096
        data[offset:offset + 5] = b'\x55\x48\x89\xe5\x90'
        struct.pack_into('<III', data, 768 + index * 12, rva, rva + 16, 0x1180)
        patches.append({'rva': hex(rva), 'original': '554889e590',
                        'code': '31c0c3', 'unwind': '01000000'})
    original = bytes(data)
    return original, {'sha256': hashlib.sha256(original).hexdigest(), 'patches': patches}


class VideoPatchTests(unittest.TestCase):
    def test_refresh_uses_active_host_modes_and_rounds_fractional_rates(self):
        modes = '   800x1280 59.93*+\n   1920x1080 144.00\n   1280x800 0.00*\n'
        self.assertEqual(video.display_refresh(modes), 60)
        self.assertEqual(video.display_refresh(modes + '   1920x1080 119.88*+\n'), 120)
        with self.assertRaisesRegex(RuntimeError, 'Cannot determine'):
            video.display_refresh('1280x800 0.00*')

    def test_refresh_reapplication_preserves_version_guard_and_user_rate_logic(self):
        original = b'prefix' + b'\xbb\x1e\0\0\0' + b'suffix'
        spec = {'sha256': video.sha256(original), 'file_offset': 6, 'original': 'bb1e000000'}
        patched = video.patch_refresh(original, spec, 60)
        self.assertEqual(patched, b'prefix' + b'\xbb\x3c\0\0\0' + b'suffix')
        self.assertEqual(video.patch_refresh(patched, spec, 90)[7:11], struct.pack('<I', 90))
        with self.assertRaisesRegex(RuntimeError, 'Unreviewed'):
            video.patch_refresh(patched + b'changed', spec, 60)
        for invalid in (0, 1001, 59.93, True):
            with self.assertRaisesRegex(RuntimeError, 'Invalid'):
                video.patch_refresh(original, spec, invalid)

    def test_unreviewed_payload_is_rejected_before_patching(self):
        original, spec = fixture()
        with self.assertRaisesRegex(RuntimeError, 'Unreviewed'):
            video.patch_d3d11(original + b'changed', spec)

    def test_query_jumps_and_helpers_have_valid_sorted_unwind_ranges(self):
        original, spec = fixture()
        patched = video.patch_d3d11(original, spec)
        _, optional, _, entries = video.sections(patched)
        self.assertEqual(len(entries), 2)
        self.assertEqual(patched[64:80], b'UU video shim   ')
        rva, size = struct.unpack_from('<II', patched, optional + 136)
        offset = video.rva_offset(rva, entries)
        functions = [struct.unpack_from('<III', patched, p)
                     for p in range(offset, offset + size, 12)]
        self.assertEqual(len(functions), 6)
        self.assertEqual(functions, sorted(functions))
        for patch in spec['patches']:
            begin = int(patch['rva'], 16)
            offset = video.rva_offset(begin, entries)
            self.assertEqual(patched[offset], 0xe9)
            target = begin + 5 + struct.unpack_from('<i', patched, offset + 1)[0]
            self.assertEqual(patched[video.rva_offset(target, entries):
                                     video.rva_offset(target, entries) + 3], b'\x31\xc0\xc3')
            old = next(record for record in functions if record[0] == begin)
            self.assertEqual(old[1], begin + 5)
            self.assertEqual(patched[video.rva_offset(old[2], entries):
                                     video.rva_offset(old[2], entries) + 4], b'\x01\0\0\0')

    def test_byte_patch_checks_both_release_hash_and_original_bytes(self):
        data = b'before'
        spec = {'sha256': video.sha256(data), 'file_offset': 0,
                'original': b'before'.hex(), 'replacement': b'after!'.hex()}
        self.assertEqual(video.patch_bytes(data, spec, 'fixture'), b'after!')
        spec['original'] = b'wrong!'.hex()
        with self.assertRaisesRegex(RuntimeError, 'Unexpected'):
            video.patch_bytes(data, spec, 'fixture')

    def test_native_queries_are_tied_to_the_reviewed_source(self):
        manifest = json.loads((ROOT / 'patches/steamos-video.json').read_text())
        self.assertEqual(manifest['helper_source_sha256'],
                         video.sha256((ROOT / 'src/uu_video_caps.c').read_bytes()))
        self.assertEqual(len(manifest['d3d11']['patches']), 3)

    def test_video_helper_unwind_matches_its_saved_nonvolatile_registers(self):
        manifest = json.loads((ROOT / 'patches/steamos-video.json').read_text())
        for patch in manifest['d3d11']['patches']:
            code, unwind = bytes.fromhex(patch['code']), bytes.fromhex(patch['unwind'])
            pushes = []
            for offset, opcode in enumerate(code):
                if not 0x50 <= opcode <= 0x57:
                    break
                pushes.append((offset + 1, opcode - 0x50))
            self.assertEqual(unwind[0], 1)
            self.assertEqual(unwind[1], len(pushes))
            self.assertEqual(unwind[2], len(pushes))
            self.assertEqual(unwind[3], 0)
            restored = [(unwind[4 + index * 2], unwind[5 + index * 2] >> 4)
                        for index in range(unwind[2])]
            self.assertEqual(restored, list(reversed(pushes)))
            self.assertTrue(all(unwind[5 + index * 2] & 15 == 0
                                for index in range(unwind[2])))


if __name__ == '__main__':
    unittest.main()
