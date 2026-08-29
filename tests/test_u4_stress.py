import unittest

from src.u4_stress import (
    U4Shock,
    U4State,
    apply_shock,
    feasibility_margin,
    shock_grid,
    stability_margin,
    stress_test,
)


class TestU4Stress(unittest.TestCase):
    def setUp(self):
        self.state = U4State(
            political=(1.0, 2.0, 3.0),
            financial=(0.1, 0.2, 0.3),
            security=(5.0, 6.0, 7.0),
            defense=(2.0, 3.0, 4.0),
            output=(10.0, 10.0, 10.0),
        )

    def test_state_requires_three_republics(self):
        self.state.validate()
        with self.assertRaises(ValueError):
            U4State((1.0,), (1.0,), (1.0,), (1.0,), (2.0,)).validate()

    def test_apply_shock_is_additive_and_deterministic(self):
        shock = U4Shock(
            financial=(0.1, -0.1, 0.0),
            political=(0.0, 0.2, 0.0),
            security=(-1.0, 0.0, 0.0),
            external_cooperation=(0.5, 0.0, 0.0),
        )
        shocked = apply_shock(self.state, shock)
        self.assertEqual(shocked.financial, (0.2, 0.1, 0.3))
        self.assertEqual(shocked.political, (1.0, 2.2, 3.0))
        self.assertEqual(shocked.security, (4.5, 6.0, 7.0))
        self.assertEqual(apply_shock(self.state, shock), shocked)

    def test_resource_feasibility_margin(self):
        self.assertEqual(feasibility_margin(self.state), 6.0)
        stressed = U4State((1.0, 2.0, 3.0), (0.1, 0.2, 0.3), (5.0, 6.0, 7.0), (2.0, 10.0, 4.0), (10.0, 10.0, 10.0))
        self.assertEqual(feasibility_margin(stressed), 0.0)

    def test_stability_margin(self):
        self.assertAlmostEqual(stability_margin(0.8), 0.2)
        self.assertGreater(stability_margin(0.8), 0.0)
        self.assertLessEqual(stability_margin(1.1), 0.0)

    def test_stress_test_positive_case(self):
        result = stress_test(self.state, U4Shock(), coupling_bound=0.8)
        self.assertTrue(result.feasible)
        self.assertTrue(result.robust)
        self.assertEqual(result.max_absolute_deviation, 0.0)

    def test_stress_test_unstable_case(self):
        result = stress_test(self.state, U4Shock(financial=(1.0, 0.0, 0.0)), coupling_bound=1.0)
        self.assertFalse(result.robust)
        self.assertEqual(result.stability_margin, 0.0)

    def test_stress_test_records_deviation(self):
        shock = U4Shock(financial=(1.0, -2.0, 0.5), political=(0.5, 0.0, -0.5))
        result = stress_test(self.state, shock, coupling_bound=0.5)
        self.assertEqual(result.state_deviation, (0.5, 0.0, -0.5, 1.0, -2.0, 0.5))
        self.assertEqual(result.max_absolute_deviation, 2.0)

    def test_shock_grid_is_complete_and_reproducible(self):
        shocks = shock_grid((-1.0, 0.0, 1.0))
        self.assertEqual(len(shocks), 12)
        self.assertEqual(shocks, shock_grid((-1.0, 0.0, 1.0)))


if __name__ == '__main__':
    unittest.main()
