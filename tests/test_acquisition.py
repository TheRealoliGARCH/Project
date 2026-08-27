import json
import tempfile
import unittest
from pathlib import Path

from src.acquisition import capture_text, load_captured_text, sha256_text


class AcquisitionTests(unittest.TestCase):
    def test_capture_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "raw.txt"
            metadata = capture_text("Official", "https://example.test", "alpha", str(target))
            text, loaded = load_captured_text(str(target))
            self.assertEqual(text, "alpha")
            self.assertEqual(metadata["sha256"], sha256_text("alpha"))
            self.assertEqual(loaded["source_name"], "Official")

    def test_checksum_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "raw.txt"
            capture_text("Official", "https://example.test", "alpha", str(target))
            target.write_text("beta", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_captured_text(str(target))


if __name__ == "__main__":
    unittest.main()
