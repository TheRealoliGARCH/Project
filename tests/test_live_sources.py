import tempfile
import unittest
from pathlib import Path

from src.acquisition import load_captured_text
from src.live_sources import acquire_official_text, extract_pipe_row


class LiveSourceBoundaryTests(unittest.TestCase):
    def test_injected_fetcher_is_captured_verbatim(self):
        seen = []
        def fetcher(url):
            seen.append(url)
            return "30/06/2026 | 1,00 | 2,00"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "official.txt"
            metadata = acquire_official_text("Official", "https://official.example/data", str(target), fetcher)
            text, loaded = load_captured_text(str(target))
        self.assertEqual(seen, ["https://official.example/data"])
        self.assertEqual(text, "30/06/2026 | 1,00 | 2,00")
        self.assertEqual(metadata["sha256"], loaded["sha256"])

    def test_empty_source_rejected(self):
        with self.assertRaises(ValueError):
            acquire_official_text("Official", "https://official.example/data", "unused.txt", lambda _: " ")

    def test_exactly_one_documented_row_required(self):
        text = "header\n2026-06-30 | 1 | 2\nfooter"
        self.assertEqual(extract_pipe_row(text, "2026-06-30"), ["2026-06-30", "1", "2"])
        with self.assertRaises(ValueError):
            extract_pipe_row(text + "\n2026-06-30 | 3 | 4", "2026-06-30")
        with self.assertRaises(ValueError):
            extract_pipe_row(text, "2026-07-01")


if __name__ == "__main__":
    unittest.main()
