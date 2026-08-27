import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "discount_factors_2025-06.csv"


class EmpiricalOutputTests(unittest.TestCase):
    def setUp(self):
        if not RESULT.exists():
            self.skipTest("empirical output not committed; run empirical/run_comparison.py first")
        with RESULT.open(newline="", encoding="utf-8") as handle:
            self.rows = list(csv.DictReader(handle))

    def test_required_columns_and_maturity_order(self):
        self.assertGreater(len(self.rows), 0)
        self.assertEqual(
            list(self.rows[0]),
            ["maturity_years", "greece_discount_factor", "italy_discount_factor", "difference_gr_minus_it"],
        )
        maturities = [float(r["maturity_years"]) for r in self.rows]
        self.assertEqual(maturities, sorted(maturities))
        self.assertEqual(len(maturities), len(set(maturities)))

    def test_discount_factor_difference_identity(self):
        for row in self.rows:
            gr = float(row["greece_discount_factor"])
            it = float(row["italy_discount_factor"])
            delta = float(row["difference_gr_minus_it"])
            self.assertGreater(gr, 0.0)
            self.assertGreater(it, 0.0)
            self.assertAlmostEqual(delta, gr - it, places=12)


if __name__ == "__main__":
    unittest.main()
