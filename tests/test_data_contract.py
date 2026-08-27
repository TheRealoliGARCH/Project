import unittest

from src.data_contract import Observation, require_common_date, validate_observations


def row(country="Greece", date="2026-07-31", maturity=3.0):
    return Observation(country, date, maturity, 0.03, "official", "benchmark_yield", "annual")


class DataContractTests(unittest.TestCase):
    def test_validation_sorts_maturities(self):
        rows = validate_observations([row(maturity=10.0), row(maturity=3.0)])
        self.assertEqual([x.maturity_years for x in rows], [3.0, 10.0])

    def test_duplicate_maturity_rejected(self):
        with self.assertRaises(ValueError):
            validate_observations([row(), row()])

    def test_common_date_required(self):
        italy = [row(country="Italy", date="2026-08-01")]
        with self.assertRaises(ValueError):
            require_common_date([row()], italy)

    def test_common_date_returned(self):
        italy = [row(country="Italy")]
        self.assertEqual(require_common_date([row()], italy), "2026-07-31")


if __name__ == "__main__":
    unittest.main()
