import math
import unittest


class TestPartialObservationTheory(unittest.TestCase):
    def test_entropy_monotonicity_identity(self):
        # H(X|S,T) = H(X|S) - I(X;T|S), with conditional mutual information >= 0.
        h_x_given_s = 1.7
        conditional_mutual_information = 0.4
        h_x_given_st = h_x_given_s - conditional_mutual_information
        self.assertLessEqual(h_x_given_st, h_x_given_s)
        self.assertAlmostEqual(h_x_given_st, 1.3)

    def test_triangulation_efficiency_bounds_for_discrete_entropy(self):
        prior_entropy = 2.0
        posterior_entropy = 0.5
        eta = 1.0 - posterior_entropy / prior_entropy
        self.assertGreaterEqual(eta, 0.0)
        self.assertLessEqual(eta, 1.0)
        self.assertAlmostEqual(eta, 0.75)

    def test_observational_equivalence_requires_equal_observations(self):
        observation = lambda x: (x[0] + x[1], x[0] - x[1])
        x = (3.0, 2.0)
        x_prime = (3.0, 2.0)
        self.assertEqual(observation(x), observation(x_prime))
        self.assertEqual(x, x_prime)

    def test_injective_observation_map_recovers_state(self):
        observation = lambda x: (x[0], x[1])
        x = (1.25, -0.75)
        candidates = [(1.25, -0.75), (1.25, 0.75), (-1.25, -0.75)]
        compatible = [candidate for candidate in candidates if observation(candidate) == observation(x)]
        self.assertEqual(compatible, [x])

    def test_recoverability_diameter_sequence(self):
        diameters = [1.0, 0.25, 0.0625, 0.015625]
        self.assertTrue(all(a > b for a, b in zip(diameters, diameters[1:])))
        self.assertTrue(math.isfinite(diameters[-1]))
        self.assertLess(diameters[-1], diameters[0])

    def test_jacobian_rank_condition_example(self):
        # H(x1,x2)=(x1+x2, x1-x2) has full-rank Jacobian.
        jacobian = ((1.0, 1.0), (1.0, -1.0))
        determinant = jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
        self.assertNotEqual(determinant, 0.0)
        self.assertEqual(abs(determinant), 2.0)


if __name__ == "__main__":
    unittest.main()
