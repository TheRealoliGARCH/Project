import unittest

from src.u2_closure import (
    default_parameters,
    financial_map,
    jacobian_fd,
    political_map,
    residual,
    security_map,
    sup_norm,
    validate_state,
)


class TestU2Closure(unittest.TestCase):
    def setUp(self):
        self.params = default_parameters()
        self.zero = (0.0, 0.0, 0.0)

    def test_three_republic_dimensions(self):
        self.assertEqual(len(political_map(self.zero, self.zero, self.params)), 3)
        self.assertEqual(len(financial_map(self.zero, self.zero, self.params)), 3)
        self.assertEqual(len(security_map(self.zero, self.zero, self.zero, self.params)), 3)

    def test_zero_state_is_fixed_point(self):
        self.assertEqual(residual(self.zero, self.zero, self.zero, self.zero, self.params), self.zero)
        self.assertEqual(sup_norm(self.zero), 0.0)

    def test_security_responds_to_defense(self):
        defense = (0.1, 0.0, 0.0)
        security = security_map(self.zero, self.zero, defense, self.params)
        self.assertEqual(security, defense)

    def test_finite_difference_jacobian_is_deterministic(self):
        def composed(r):
            p = political_map(r, self.zero, self.params)
            return financial_map(p, self.zero, self.params)

        jacobian_1 = jacobian_fd(composed, self.zero)
        jacobian_2 = jacobian_fd(composed, self.zero)
        self.assertEqual(jacobian_1, jacobian_2)
        self.assertEqual(len(jacobian_1), 3)
        self.assertEqual(len(jacobian_1[0]), 3)

    def test_nonfinite_states_rejected(self):
        with self.assertRaises(ValueError):
            validate_state((float('nan'), 0.0, 0.0))
        with self.assertRaises(ValueError):
            validate_state((0.0, float('inf'), 0.0))

    def test_exactly_three_republics_required(self):
        with self.assertRaises(ValueError):
            default_parameters(4)


if __name__ == '__main__':
    unittest.main()
