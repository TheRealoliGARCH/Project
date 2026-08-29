import unittest

from src.u6_uniqueness import (
    conic_jacobian_symmetry_condition,
    contraction_certificate,
    fixed_point_residual,
    infinity_norm,
    invariant_box,
    jacobian_two_conics,
    numerical_jacobian,
)


class TestU6Uniqueness(unittest.TestCase):
    def test_conic_jacobian_matches_formula(self):
        jac = jacobian_two_conics(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.assertEqual(jac, ((26.0, 60.0), (54.0, 76.0)))

    def test_transpose_symmetry_condition(self):
        self.assertTrue(conic_jacobian_symmetry_condition(1, 2, 3, 5, 7, 4, 1, 4))
        self.assertFalse(conic_jacobian_symmetry_condition(1, 2, 3, 5, 7, 4, 1, 5))

    def test_divisibility_by_four_reference(self):
        jac = jacobian_two_conics(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.assertTrue(all(value % 4 == 0 for row in jac for value in row))

    def test_numerical_jacobian(self):
        def map_fn(x):
            return (0.2 * x[0] + 0.1 * x[1], 0.3 * x[0] + 0.4 * x[1])
        jac = numerical_jacobian(map_fn, (1.0, 2.0))
        self.assertAlmostEqual(jac[0][0], 0.2, places=6)
        self.assertAlmostEqual(jac[0][1], 0.1, places=6)
        self.assertAlmostEqual(jac[1][0], 0.3, places=6)
        self.assertAlmostEqual(jac[1][1], 0.4, places=6)

    def test_contraction_certificate(self):
        self.assertTrue(contraction_certificate(0.8).unique_fixed_point)
        self.assertFalse(contraction_certificate(1.0).unique_fixed_point)
        self.assertFalse(contraction_certificate(1.2).unique_fixed_point)

    def test_infinity_norm(self):
        self.assertAlmostEqual(infinity_norm(((0.2, 0.1), (0.3, 0.4))), 0.7)

    def test_fixed_point_residual(self):
        def map_fn(x):
            return (0.5 * x[0], 0.5 * x[1])
        self.assertEqual(fixed_point_residual(map_fn, (2.0, 4.0)), (-1.0, -2.0))

    def test_invariant_box(self):
        def map_fn(x):
            return (0.5 * x[0], 0.5 * x[1])
        self.assertTrue(invariant_box(map_fn, (0.0, 0.0), (2.0, 2.0), ((0.0, 0.0), (2.0, 2.0))))
        self.assertFalse(invariant_box(map_fn, (0.0, 0.0), (0.5, 0.5), ((2.0, 2.0),)))

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            contraction_certificate(-0.1)
        with self.assertRaises(ValueError):
            infinity_norm(((1.0, 2.0),))
        with self.assertRaises(ValueError):
            numerical_jacobian(lambda x: x, (1.0,), step=0.0)


if __name__ == "__main__":
    unittest.main()
