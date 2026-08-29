import unittest

from src.u3_optimality import (
    U3Parameters,
    check_resource_allocation,
    resource_constraint,
    security_power,
    strategic_allocation_residual,
    validate_u3_point,
    welfare,
    welfare_foc_residual,
    welfare_soc,
)


class TestU3Optimality(unittest.TestCase):
    def setUp(self):
        self.params = U3Parameters(
            output=10.0,
            preference_security=0.5,
            threat=0.0,
            external_security=0.0,
        )

    def test_resource_constraint(self):
        self.assertEqual(resource_constraint(10.0, 4.0), 6.0)
        with self.assertRaises(ValueError):
            resource_constraint(10.0, 11.0)

    def test_welfare_is_finite_at_interior_point(self):
        value = welfare(10.0, 4.0, 0.5, security_power, 0.0, 0.0)
        self.assertTrue(value == value)

    def test_foc_and_soc_at_benchmark_optimum(self):
        # With S = 1 + sqrt(G), Y=10 and alpha=1/2,
        # the analytic interior optimum is G=4.
        foc = welfare_foc_residual(
            10.0, 4.0, 0.5, security_power, 0.0, 0.0, step=1e-5
        )
        soc = welfare_soc(
            10.0, 4.0, 0.5, security_power, 0.0, 0.0, step=1e-4
        )
        self.assertAlmostEqual(foc, 0.0, places=7)
        self.assertLess(soc, 0.0)

    def test_security_responds_to_defense(self):
        low = security_power(1.0, 0.0, 0.0)
        high = security_power(4.0, 0.0, 0.0)
        self.assertGreater(high, low)

    def test_external_security_reduces_required_domestic_resources(self):
        no_help = security_power(4.0, 0.0, 0.0)
        with_help = security_power(4.0, 0.0, 2.0)
        self.assertGreater(with_help, no_help)

    def test_strategic_allocation_consistency(self):
        weights = (0.5, 0.5, 0.0, 0.0)
        states = (0.0, 10.0, 20.0, 30.0)
        self.assertTrue(check_resource_allocation(weights, states, 5.0))
        self.assertEqual(strategic_allocation_residual(weights, states, 5.0), (0.0, 0.0))

    def test_invalid_strategy_rejected(self):
        weights = (0.8, 0.8, 0.0, 0.0)
        states = (0.0, 10.0, 20.0, 30.0)
        self.assertFalse(check_resource_allocation(weights, states, 5.0))

    def test_candidate_validation(self):
        validate_u3_point(self.params, 4.0, security_power)
        with self.assertRaises(ValueError):
            validate_u3_point(self.params, 10.0, security_power)


if __name__ == '__main__':
    unittest.main()
