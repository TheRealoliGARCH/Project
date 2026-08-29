import unittest

from src.u56_interface import (
    U56InterfaceError,
    build_identification_result,
    identification_to_equilibrium_restrictions,
    validate_no_uniqueness_inference,
)


class TestU56Interface(unittest.TestCase):
    def result(self):
        return build_identification_result(
            ("alpha", "beta", "gamma"),
            (1.0, 2.0, 3.0),
            (True, False, True),
            (0.1, 0.2, 0.3),
            provenance="U5 identification analysis",
        )

    def test_only_identified_parameters_cross_interface(self):
        restrictions = identification_to_equilibrium_restrictions(self.result())
        self.assertEqual(restrictions.parameter_names, ("alpha", "gamma"))
        self.assertEqual(restrictions.restrictions, (1.0, 3.0))
        self.assertEqual(restrictions.uncertainty, (0.1, 0.3))

    def test_identification_does_not_certify_uniqueness(self):
        restrictions = identification_to_equilibrium_restrictions(self.result())
        self.assertFalse(restrictions.uniqueness_certified)
        validate_no_uniqueness_inference(restrictions)

    def test_false_uniqueness_certificate_fails(self):
        restrictions = identification_to_equilibrium_restrictions(self.result())
        object.__setattr__(restrictions, "uniqueness_certified", True)
        with self.assertRaises(U56InterfaceError):
            validate_no_uniqueness_inference(restrictions)

    def test_all_unidentified_parameters_fail(self):
        result = build_identification_result(
            ("alpha",), (1.0,), (False,), (0.1,), provenance="U5"
        )
        with self.assertRaises(U56InterfaceError):
            identification_to_equilibrium_restrictions(result)

    def test_mismatched_lengths_fail(self):
        with self.assertRaises(U56InterfaceError):
            build_identification_result(
                ("alpha", "beta"), (1.0,), (True, True), (0.1, 0.2), provenance="U5"
            )

    def test_negative_uncertainty_fails(self):
        with self.assertRaises(U56InterfaceError):
            build_identification_result(
                ("alpha",), (1.0,), (True,), (-0.1,), provenance="U5"
            )

    def test_missing_provenance_fails(self):
        with self.assertRaises(U56InterfaceError):
            build_identification_result(
                ("alpha",), (1.0,), (True,), (0.1,), provenance=""
            )


if __name__ == "__main__":
    unittest.main()
