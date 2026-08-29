import math
import unittest

from src.nss import NSSParameters, loadings, spot_yield


class TestNSSLoadings(unittest.TestCase):
    def test_loadings_match_spot_yield_basis(self):
        maturity = 5.0
        p = NSSParameters(0.02, -0.01, 0.03, 0.01, 1.5, 4.0)
        basis = loadings(maturity, p.tau1, p.tau2)
        expected = sum(beta * loading for beta, loading in zip(
            (p.beta0, p.beta1, p.beta2, p.beta3), basis
        ))
        self.assertAlmostEqual(spot_yield(maturity, p), expected, places=14)

    def test_small_ratio_loading_is_finite_and_matches_series(self):
        maturity = 1e-12
        basis = loadings(maturity, 1.0, 2.0)
        self.assertEqual(len(basis), 4)
        self.assertTrue(all(math.isfinite(value) for value in basis))
        x = maturity
        expected = 1.0 - x / 2.0 + x * x / 6.0
        self.assertAlmostEqual(basis[1], expected, places=15)

    def test_loadings_reject_invalid_parameters(self):
        with self.assertRaises(ValueError):
            loadings(1.0, 0.0, 1.0)
        with self.assertRaises(ValueError):
            loadings(-1.0, 1.0, 2.0)


if __name__ == "__main__":
    unittest.main()
