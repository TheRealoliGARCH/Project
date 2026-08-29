import unittest

from src.u23_interface import (
    REPUBLICS,
    U23InterfaceError,
    u2_to_u3_baseline,
    validate_u3_resource_feasibility,
)


class TestU23Interface(unittest.TestCase):
    def setUp(self):
        self.state = {
            "r": (0.02, 0.04, 0.06),
            "p": (0.1, 0.2, 0.3),
            "s": (0.4, 0.5, 0.6),
            "g": (2.0, 3.0, 4.0),
        }

    def test_canonical_republic_order(self):
        self.assertEqual(REPUBLICS, ("Greece", "India", "Italy"))

    def test_u2_fields_are_preserved(self):
        baseline = u2_to_u3_baseline(self.state)
        self.assertEqual(baseline, self.state)

    def test_missing_field_fails_explicitly(self):
        state = dict(self.state)
        del state["s"]
        with self.assertRaises(U23InterfaceError):
            u2_to_u3_baseline(state)

    def test_wrong_dimension_fails_explicitly(self):
        state = dict(self.state)
        state["g"] = (2.0, 3.0)
        with self.assertRaises(U23InterfaceError):
            u2_to_u3_baseline(state)

    def test_nonfinite_field_fails_explicitly(self):
        state = dict(self.state)
        state["p"] = (0.1, float("inf"), 0.3)
        with self.assertRaises(U23InterfaceError):
            u2_to_u3_baseline(state)

    def test_resource_constraint_is_preserved(self):
        baseline = u2_to_u3_baseline(self.state)
        self.assertEqual(validate_u3_resource_feasibility(baseline, (10.0, 10.0, 10.0)), (8.0, 7.0, 6.0))

    def test_resource_constraint_failure_is_explicit(self):
        baseline = u2_to_u3_baseline(self.state)
        with self.assertRaises(U23InterfaceError):
            validate_u3_resource_feasibility(baseline, (1.0, 2.0, 3.0))


if __name__ == "__main__":
    unittest.main()
