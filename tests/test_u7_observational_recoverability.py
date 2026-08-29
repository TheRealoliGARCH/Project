import unittest

from src.u7_observational_recoverability import (
    ObservationalRecoverabilityError,
    assess_recoverability,
    build_observation_map,
    require_recoverability,
)


class TestObservationalRecoverability(unittest.TestCase):
    def setUp(self):
        self.operator = build_observation_map((0, 2))

    def test_observation_operator_is_deterministic(self):
        state = (1.0, 2.0, 3.0)
        self.assertEqual(self.operator.apply(state), (1.0, 3.0))
        self.assertEqual(self.operator.apply(state), (1.0, 3.0))

    def test_distinct_states_with_distinct_observations_are_identifiable(self):
        result = assess_recoverability(self.operator, (1.0, 2.0, 3.0), (1.0, 4.0, 5.0))
        self.assertFalse(result.observations_equal)
        self.assertTrue(result.identifiable)

    def test_distinct_states_with_equal_observations_are_not_recoverable(self):
        result = assess_recoverability(self.operator, (1.0, 2.0, 3.0), (1.0, 9.0, 3.0))
        self.assertTrue(result.observations_equal)
        self.assertFalse(result.latent_states_equal)
        self.assertFalse(result.identifiable)

    def test_identical_states_are_recoverable(self):
        result = assess_recoverability(self.operator, (1.0, 2.0, 3.0), (1.0, 2.0, 3.0))
        self.assertTrue(result.observations_equal)
        self.assertTrue(result.latent_states_equal)
        self.assertTrue(result.identifiable)

    def test_require_recoverability_rejects_ambiguous_reference(self):
        with self.assertRaises(ObservationalRecoverabilityError):
            require_recoverability(self.operator, (1.0, 2.0, 3.0), reference_state=(1.0, 9.0, 3.0))

    def test_invalid_observation_index_fails(self):
        operator = build_observation_map((0, 3))
        with self.assertRaises(ObservationalRecoverabilityError):
            operator.apply((1.0, 2.0, 3.0))

    def test_duplicate_indices_fail(self):
        with self.assertRaises(ObservationalRecoverabilityError):
            build_observation_map((0, 0))

    def test_negative_index_fails(self):
        with self.assertRaises(ObservationalRecoverabilityError):
            build_observation_map((-1, 0))

    def test_dimension_mismatch_fails(self):
        with self.assertRaises(ObservationalRecoverabilityError):
            assess_recoverability(self.operator, (1.0, 2.0), (1.0, 2.0, 3.0))


if __name__ == "__main__":
    unittest.main()
