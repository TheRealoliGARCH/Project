import unittest

from src.u34_interface import (
    REPUBLICS,
    U34InterfaceError,
    u3_to_u4_baseline,
    validate_consumption_identity,
)


class TestU34Interface(unittest.TestCase):
    def setUp(self):
        self.state = {
            "p": (0.1, 0.2, 0.3),
            "r": (0.02, 0.04, 0.06),
            "s": (0.4, 0.5, 0.6),
            "G_m": (2.0, 3.0, 4.0),
            "Y": (10.0, 12.0, 15.0),
        }

    def test_canonical_republic_order(self):
        self.assertEqual(REPUBLICS, ("Greece", "India", "Italy"))

    def test_u3_fields_are_preserved(self):
        self.assertEqual(u3_to_u4_baseline(self.state), self.state)

    def test_consumption_identity_is_preserved(self):
        self.assertEqual(validate_consumption_identity(self.state), (8.0, 9.0, 11.0))

    def test_boundary_zero_military_allocation_is_valid(self):
        state = dict(self.state)
        state["G_m"] = (0.0, 0.0, 0.0)
        self.assertEqual(validate_consumption_identity(state), state["Y"])

    def test_boundary_full_allocation_is_valid(self):
        state = dict(self.state)
        state["G_m"] = state["Y"]
        self.assertEqual(validate_consumption_identity(state), (0.0, 0.0, 0.0))

    def test_military_allocation_above_output_fails(self):
        state = dict(self.state)
        state["G_m"] = (11.0, 3.0, 4.0)
        with self.assertRaises(U34InterfaceError):
            u3_to_u4_baseline(state)

    def test_negative_military_allocation_fails(self):
        state = dict(self.state)
        state["G_m"] = (-1.0, 3.0, 4.0)
        with self.assertRaises(U34InterfaceError):
            u3_to_u4_baseline(state)

    def test_missing_field_fails_explicitly(self):
        state = dict(self.state)
        del state["Y"]
        with self.assertRaises(U34InterfaceError):
            u3_to_u4_baseline(state)

    def test_wrong_dimension_fails_explicitly(self):
        state = dict(self.state)
        state["G_m"] = (2.0, 3.0)
        with self.assertRaises(U34InterfaceError):
            u3_to_u4_baseline(state)

    def test_nonfinite_field_fails_explicitly(self):
        state = dict(self.state)
        state["Y"] = (10.0, float("nan"), 15.0)
        with self.assertRaises(U34InterfaceError):
            u3_to_u4_baseline(state)


if __name__ == "__main__":
    unittest.main()
