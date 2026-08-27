import unittest
from pathlib import Path

from src.acquisition import capture_text, load_captured_text
from src.data_contract import require_common_date
from src.parsers import parse_bank_of_greece_row, parse_banca_d_italia_bmk0100_row

FIXTURES = Path(__file__).parent / "fixtures"


class FixtureIntegrationTests(unittest.TestCase):
    def test_capture_parse_validate_end_to_end(self):
        greek_text = (FIXTURES / "bank_of_greece_sample.txt").read_text(encoding="utf-8").strip()
        italian_text = (FIXTURES / "banca_d_italia_bmk0100_sample.txt").read_text(encoding="utf-8").strip()

        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            gr_path = Path(tmp) / "gr.txt"
            it_path = Path(tmp) / "it.txt"
            capture_text("Bank of Greece fixture", "fixture://gr", greek_text, str(gr_path))
            capture_text("Banca d'Italia fixture", "fixture://it", italian_text, str(it_path))
            gr_loaded, _ = load_captured_text(str(gr_path))
            it_loaded, _ = load_captured_text(str(it_path))

        gr_cells = [x.strip() for x in gr_loaded.split("|")][1:]
        it_cells = [x.strip() for x in it_loaded.split("|")][1:]
        gr = parse_bank_of_greece_row("2026-06-30", gr_cells, "fixture://gr")
        it = parse_banca_d_italia_bmk0100_row("2026-06-30", it_cells, "fixture://it")

        self.assertEqual(require_common_date(gr, it), "2026-06-30")
        self.assertEqual(len(gr), 7)
        self.assertEqual(len(it), 4)
        self.assertAlmostEqual(gr[0].yield_value, 0.029)
        self.assertAlmostEqual(it[0].yield_value, 0.02436)


if __name__ == "__main__":
    unittest.main()
