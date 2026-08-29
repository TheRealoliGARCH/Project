import unittest

from src.u5_causal import (
    ate,
    difference_in_differences,
    frequentist_effect,
    ghoshian_transform,
    normal_normal_posterior,
    posterior_probability_positive,
)


class TestU5Causal(unittest.TestCase):
    def test_ghoshian_transform_known_value(self):
        self.assertAlmostEqual(ghoshian_transform(0.0, 1.0, 2.0, 1.0, 0.0), 1.0 + 2.718281828459045)

    def test_ate_known_contrast(self):
        self.assertAlmostEqual(ate([3.0, 5.0, 7.0], [1.0, 2.0, 3.0]), 3.0)

    def test_did_known_effect(self):
        self.assertAlmostEqual(
            difference_in_differences([1, 2], [5, 6], [1, 2], [2, 3]), 3.0
        )

    def test_frequentist_effect_matches_ate(self):
        treated = [4.0, 5.0, 6.0, 5.0]
        control = [1.0, 2.0, 3.0, 2.0]
        estimate = frequentist_effect(treated, control)
        self.assertAlmostEqual(estimate.effect, ate(treated, control))
        self.assertGreater(estimate.standard_error, 0.0)
        self.assertGreaterEqual(estimate.p_value_two_sided, 0.0)
        self.assertLessEqual(estimate.p_value_two_sided, 1.0)

    def test_normal_normal_posterior_is_deterministic(self):
        a = normal_normal_posterior(2.0, 0.5, 0.0, 1.0)
        b = normal_normal_posterior(2.0, 0.5, 0.0, 1.0)
        self.assertEqual(a, b)
        self.assertGreater(a[1], 0.0)

    def test_positive_posterior_probability(self):
        mean, sd = normal_normal_posterior(2.0, 0.5)
        probability = posterior_probability_positive(mean, sd)
        self.assertGreater(probability, 0.5)
        self.assertLessEqual(probability, 1.0)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            ate([], [1.0])
        with self.assertRaises(ValueError):
            ghoshian_transform(1.0, 0.0, 0.0, 1.0, 0.0)
        with self.assertRaises(ValueError):
            normal_normal_posterior(1.0, 0.0)


if __name__ == "__main__":
    unittest.main()
