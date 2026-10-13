import hashlib
from pathlib import Path
import tempfile
import unittest
from halveth_xof1296 import DOMAIN, OUTPUT_BYTES, cli, fingerprint


class TestHash1296(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = Path(self.tmp.name) / "sample.bin"
        self.p.write_bytes(b"HALVETH DNA")

    def test_length_and_exact_digest(self):
        data = self.p.read_bytes()
        obj = fingerprint(self.p)
        self.assertEqual(obj["shake256_1296"], hashlib.shake_256(DOMAIN + data).hexdigest(162))
        self.assertEqual(len(obj["shake256_1296"]), 324)
        self.assertEqual(obj["shake256_output_bits"], 1296)

    def test_sha256_compatible(self):
        self.assertEqual(fingerprint(self.p)["sha256"], hashlib.sha256(self.p.read_bytes()).hexdigest())

    def test_tampering_changes_id(self):
        a = fingerprint(self.p)["shake256_1296"]
        self.p.write_bytes(b"HALVETH DNB")
        self.assertNotEqual(a, fingerprint(self.p)["shake256_1296"])

    def test_expected_matches(self):
        good = fingerprint(self.p)["shake256_1296"]
        self.assertEqual(cli([str(self.p), "--expected", good]), 0)
        self.assertEqual(cli([str(self.p), "--expected", "0" * 324]), 1)

    def test_rejects_missing(self):
        with self.assertRaises(ValueError):
            fingerprint(self.p / "absent")

    def test_rejects_symlink(self):
        sym = Path(self.tmp.name) / "alias"
        try:
            sym.symlink_to(self.p)
        except OSError:
            self.skipTest("symlink unsupported")
        with self.assertRaises(ValueError):
            fingerprint(sym)


if __name__ == "__main__":
    unittest.main()
