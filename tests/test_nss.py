import math
import unittest

from src.nss import NSSParameters, discount_factor, rmse, spot_yield


class TestNSS(unittest.TestCase):
    def setUp(self):
        self.p = NSSParameters(0.04, -0.01, 0.02, -0.005, 2.0, 10.0)

    def test_discount_factor_at_zero_is_one(self):
        self.assertAlmostEqual(discount_factor(0.0, self.p), 1.0)

    def test_positive_maturity_discount_factor_positive(self):
        self.assertGreater(discount_factor(10.0, self.p), 0.0)

    def test_long_run_spot_yield_converges_to_beta0(self):
        self.assertAlmostEqual(spot_yield(1_000_000.0, self.p), self.p.beta0, places=5)

    def test_invalid_tau_rejected(self):
        with self.assertRaises(ValueError):
            spot_yield(5.0, NSSParameters(0, 0, 0, 0, 0, 1))

    def test_rmse(self):
        self.assertAlmostEqual(rmse([1.0, 2.0], [1.0, 4.0]), math.sqrt(2.0))


if __name__ == "__main__":
    unittest.main()
