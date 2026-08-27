import unittest

from src.parsers import parse_bank_of_greece_row, parse_banca_d_italia_bmk0100_row


class ParserTests(unittest.TestCase):
    def test_bank_of_greece_price_yield_pairs(self):
        cells = [
            "103,61", "2,36", "95,16", "2,65", "92,63", "3,01",
            "101,45", "3,44", "106,66", "3,70", "104,20", "3,84",
            "97,68", "4,27",
        ]
        rows = parse_bank_of_greece_row("2025-12-31", cells, "Bank of Greece")
        self.assertEqual([row.maturity_years for row in rows], [3, 5, 7, 10, 15, 20, 30])
        self.assertAlmostEqual(rows[0].yield_decimal, 0.0236)
        self.assertAlmostEqual(rows[-1].yield_decimal, 0.0427)

    def test_bank_of_greece_rejects_wrong_shape(self):
        with self.assertRaises(ValueError):
            parse_bank_of_greece_row("2025-12-31", ["1"] * 13, "Bank of Greece")

    def test_banca_d_italia_bmk0100_with_optional_cct(self):
        rows = parse_banca_d_italia_bmk0100_row(
            "2025-12-31", ["2.436", "2.843", "3.589", "4.409", "3.426"],
            "Banca d'Italia BMK0100",
        )
        self.assertEqual([row.maturity_years for row in rows], [3, 5, 10, 30])
        self.assertAlmostEqual(rows[0].yield_decimal, 0.02436)
        self.assertAlmostEqual(rows[-1].yield_decimal, 0.04409)

    def test_banca_d_italia_rejects_missing_yield(self):
        with self.assertRaises(ValueError):
            parse_banca_d_italia_bmk0100_row(
                "2025-12-31", ["2.436", "-", "3.589", "4.409"], "Banca d'Italia"
            )


if __name__ == "__main__":
    unittest.main()
