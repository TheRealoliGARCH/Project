import unittest

from src.sources import bank_of_greece_observations, banca_d_italia_observations


class SourceAdapterTests(unittest.TestCase):
    def test_greek_adapter_normalizes_percentages_and_metadata(self):
        rows = bank_of_greece_observations(
            "2026-07-31",
            [{"maturity_years": 3, "yield_percent": 2.90}],
        )
        self.assertEqual(rows[0].country, "Greece")
        self.assertAlmostEqual(rows[0].yield_decimal, 0.029)
        self.assertEqual(rows[0].source, "Bank of Greece")

    def test_italian_adapter_normalizes_percentages_and_metadata(self):
        rows = banca_d_italia_observations(
            "2026-07-31",
            [{"maturity_years": 5, "yield_percent": 3.20}],
        )
        self.assertEqual(rows[0].country, "Italy")
        self.assertAlmostEqual(rows[0].yield_decimal, 0.032)
        self.assertEqual(rows[0].source, "Banca d'Italia")

    def test_records_require_explicit_fields(self):
        with self.assertRaises(ValueError):
            bank_of_greece_observations("2026-07-31", [{"maturity_years": 3}])


if __name__ == "__main__":
    unittest.main()
