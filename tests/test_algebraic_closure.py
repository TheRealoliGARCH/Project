import unittest

from src.algebraic_closure import (
    closure_residual,
    permutation_invariant,
    polynomial_value,
    symmetric_invariants,
)


class TestAlgebraicClosure(unittest.TestCase):
    def setUp(self):
        self.rates = (0.02, 0.035, 0.05)

    def test_symmetric_invariants(self):
        r_a, r_b, r_c = symmetric_invariants(self.rates)
        self.assertAlmostEqual(r_a, 0.105)
        self.assertAlmostEqual(r_b, 0.0032)
        self.assertAlmostEqual(r_c, 0.000035)

    def test_vieta_cubic_vanishes_at_each_rate(self):
        invariants = symmetric_invariants(self.rates)
        for rate in self.rates:
            self.assertAlmostEqual(polynomial_value(rate, invariants), 0.0, places=14)

    def test_closure_residual_is_zero_to_floating_point_precision(self):
        self.assertLess(closure_residual(self.rates), 1e-14)

    def test_permutation_invariance(self):
        self.assertTrue(permutation_invariant(self.rates))

    def test_wrong_rate_does_not_pass_as_a_root(self):
        invariants = symmetric_invariants(self.rates)
        self.assertNotAlmostEqual(polynomial_value(0.08, invariants), 0.0, places=12)

    def test_requires_three_rates(self):
        with self.assertRaises(ValueError):
            symmetric_invariants((0.02, 0.035))


if __name__ == "__main__":
    unittest.main()
