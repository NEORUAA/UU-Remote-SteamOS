import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("terminal_runtime", ROOT / "scripts/manage-terminal-runtime.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TerminalRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runtime = MODULE.TerminalRuntime(self.root / "prefix with spaces")
        self.runtime.bin.mkdir(parents=True)
        self.runtime.system.mkdir(parents=True)
        self.runtime.compat.mkdir(parents=True)
        self.vendor = b"owned test vendor ConPTY"
        self.builtin = b"MZ" + b"\0" * 62 + b"Wine builtin DLL" + b"owned shell"
        self.runtime.conpty.write_bytes(self.vendor)
        self.runtime.shell.write_bytes(self.builtin)
        self.runtime.shell.chmod(0o700)
        self.build = self.root / "build"
        self.build.mkdir()
        (self.build / "uu-conpty-compat.dll").write_bytes(b"owned compatibility v1")
        patcher = patch.object(MODULE, "VENDOR_CONPTY_SHA256", hashlib.sha256(self.vendor).hexdigest())
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_install_upgrade_restore_preserves_originals_and_aliases(self):
        self.runtime.install(self.build)
        self.runtime.verify()
        self.assertEqual(self.runtime.original.read_bytes(), self.vendor)
        self.assertEqual(self.runtime.shell_original.read_bytes(), self.builtin)
        self.assertEqual(self.runtime.shell_original.stat().st_mode & 0o777, 0o700)
        (self.build / "uu-conpty-compat.dll").write_bytes(b"owned compatibility v2")
        self.runtime.install(self.build)
        self.runtime.verify()
        self.assertEqual(self.runtime.original.read_bytes(), self.vendor)
        self.runtime.restore(dry_run=True)
        self.assertTrue(self.runtime.shell.is_symlink())
        self.runtime.restore()
        self.assertEqual(self.runtime.conpty.read_bytes(), self.vendor)
        self.assertEqual(self.runtime.shell.read_bytes(), self.builtin)
        self.assertFalse(self.runtime.links[1][0].exists())

    def test_unknown_vendor_dll_is_rejected_before_writes(self):
        self.runtime.conpty.write_bytes(b"user supplied DLL")
        with self.assertRaisesRegex(ValueError, "Unmanaged"):
            self.runtime.install(self.build)
        self.assertFalse(self.runtime.original.exists())
        self.assertEqual(self.runtime.shell.read_bytes(), self.builtin)

    def test_foreign_system_link_is_preserved_on_failure(self):
        self.runtime.shell.unlink()
        foreign = self.root / "user powershell"
        foreign.write_bytes(b"user binary")
        self.runtime.shell.symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, "Unmanaged terminal link"):
            self.runtime.install(self.build)
        self.assertFalse(self.runtime.original.exists())
        self.assertEqual(self.runtime.shell.resolve(), foreign)

    def test_wineboot_detach_prevents_following_alias_into_proxy(self):
        self.runtime.install(self.build)
        self.runtime.detach_system_links()
        self.assertFalse(self.runtime.shell.is_symlink())
        self.assertEqual(self.runtime.shell.read_bytes(), self.builtin)
        upgraded = self.builtin + b" new Wine version"
        self.runtime.shell.write_bytes(upgraded)
        self.runtime.install(self.build)
        self.runtime.restore()
        self.assertEqual(self.runtime.shell.read_bytes(), upgraded)

    def test_verify_detects_changed_managed_dll(self):
        self.runtime.install(self.build)
        self.runtime.managed.write_bytes(b"stale mirror")
        with self.assertRaises(ValueError):
            self.runtime.verify()


if __name__ == "__main__":
    unittest.main()
