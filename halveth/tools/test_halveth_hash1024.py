import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import halveth_hash1024 as h


class TestHalvethIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "code"
        self.root.mkdir()
        (self.root / "alpha.txt").write_bytes(b"abc")

    def test_file_fingerprint(self):
        record = h.snapshot(self.root)["files"][0]
        self.assertEqual(record["sha256"], hashlib.sha256(b"abc").hexdigest())
        self.assertEqual(len(record["shake256_1024"]), 256)
        self.assertEqual(record["shake256_1024"], hashlib.shake_256(h.DOMAIN + b"abc").hexdigest(128))
        self.assertEqual(record["bytes"], 3)

    def test_unchanged_tree_verifies(self):
        first = h.snapshot(self.root)
        self.assertTrue(h.verify(self.root, first)["ok"])

    def test_detects_tamper(self):
        old = h.snapshot(self.root)
        (self.root / "alpha.txt").write_bytes(b"abd")
        result = h.verify(self.root, old)
        self.assertEqual(result["changed"], ["alpha.txt"])
        self.assertFalse(result["ok"])

    def test_detects_missing_and_new(self):
        old = h.snapshot(self.root)
        (self.root / "alpha.txt").unlink()
        (self.root / "beta.txt").write_text("new")
        result = h.verify(self.root, old)
        self.assertEqual(result["missing"], ["alpha.txt"])
        self.assertEqual(result["extra"], ["beta.txt"])

    def test_excludes_common_secret_and_build_files(self):
        (self.root / ".env").write_text("secret=123")
        (self.root / "private.pem").write_text("not a real key")
        (self.root / "build").mkdir()
        (self.root / "build" / "out.txt").write_text("build output")
        self.assertEqual([f["path"] for f in h.snapshot(self.root)["files"]], ["alpha.txt"])

    def test_output_outside_root(self):
        inside = self.root / "manifest.json"
        self.assertEqual(h.main(["snapshot", str(self.root), "--out", str(inside)]), 2)
        self.assertFalse(inside.exists())
        outside = Path(self.tmp.name) / "manifest.json"
        self.assertEqual(h.main(["snapshot", str(self.root), "--out", str(outside)]), 0)
        self.assertTrue(outside.exists())
        self.assertEqual(h.main(["verify", str(self.root), str(outside)]), 0)
        self.assertEqual(json.loads(outside.read_text())["schema"], h.SCHEMA)

    def test_symlink_not_followed(self):
        external = Path(self.tmp.name) / "external.txt"
        external.write_text("outside")
        try:
            (self.root / "alias.txt").symlink_to(external)
        except OSError:
            self.skipTest("Host does not support unprivileged symlinks")
        self.assertEqual([f["path"] for f in h.snapshot(self.root)["files"]], ["alpha.txt"])

    def test_reject_wrong_schema_and_duplicates(self):
        m = h.snapshot(self.root)
        m["schema"] = "unknown"
        with self.assertRaises(ValueError):
            h.verify(self.root, m)
        m = h.snapshot(self.root)
        m["files"].append(m["files"][0])
        with self.assertRaises(ValueError):
            h.verify(self.root, m)


if __name__ == "__main__":
    unittest.main()
