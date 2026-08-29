import unittest

from src.u12_interface import (
    U12InterfaceError,
    symmetric_invariants,
    u1_to_u2_financial_state,
    validate_symmetric_closure,
)


class TestU12Interface(unittest.TestCase):
    def test_ordered_rates_are_preserved_for_u2(self):
        rates = (0.02, 0.04, 0.06)  # Greece, India, Italy
        self.assertEqual(u1_to_u2_financial_state(rates), rates)

    def test_symmetric_invariants_are_computed_exactly(self):
        rates = (1.0, 2.0, 3.0)
        self.assertEqual(symmetric_invariants(rates), (6.0, 11.0, 6.0))

    def test_invariants_validate_against_upstream_rates(self):
        rates = (1.0, 2.0, 3.0)
        validate_symmetric_closure(rates, (6.0, 11.0, 6.0))

    def test_invariants_cannot_replace_ordered_country_labels(self):
        rates = (1.0, 2.0, 3.0)
        permuted = (3.0, 1.0, 2.0)
        self.assertEqual(symmetric_invariants(rates), symmetric_invariants(permuted))
        self.assertNotEqual(u1_to_u2_financial_state(rates), u1_to_u2_financial_state(permuted))

    def test_wrong_dimension_fails_explicitly(self):
        with self.assertRaises(U12InterfaceError):
            u1_to_u2_financial_state((1.0, 2.0))

    def test_nonfinite_value_fails_explicitly(self):
        with self.assertRaises(U12InterfaceError):
            u1_to_u2_financial_state((1.0, float("nan"), 3.0))

    def test_wrong_invariants_fail_explicitly(self):
        with self.assertRaises(U12InterfaceError):
            validate_symmetric_closure((1.0, 2.0, 3.0), (6.0, 10.0, 6.0))


if __name__ == "__main__":
    unittest.main()
