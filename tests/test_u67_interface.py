import unittest

from src.u67_interface import (
    U67InterfaceError,
    build_uniqueness_certificate,
    validate_u7_certificate,
)


class TestU67Interface(unittest.TestCase):
    def certificate(self):
        return build_uniqueness_certificate(
            (0.2, 0.3, 0.4),
            0.75,
            (0.0, 0.0, 0.0),
            (1.0, 1.0, 1.0),
            certified=True,
            provenance="U6 contraction certificate",
        )

    def test_certified_contraction_crosses_interface(self):
        certificate = self.certificate()
        validate_u7_certificate(certificate)
        self.assertTrue(certificate.certified)

    def test_equilibrium_and_domain_are_preserved(self):
        certificate = self.certificate()
        self.assertEqual(certificate.equilibrium, (0.2, 0.3, 0.4))
        self.assertEqual(certificate.domain_lower, (0.0, 0.0, 0.0))
        self.assertEqual(certificate.domain_upper, (1.0, 1.0, 1.0))

    def test_noncontractive_bound_cannot_be_certified(self):
        with self.assertRaises(U67InterfaceError):
            build_uniqueness_certificate(
                (0.2, 0.3, 0.4), 1.0,
                (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
                certified=True, provenance="U6"
            )

    def test_uncertified_result_cannot_enter_u7_as_unique(self):
        certificate = build_uniqueness_certificate(
            (0.2, 0.3, 0.4), 0.75,
            (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
            certified=False, provenance="U6"
        )
        with self.assertRaises(U67InterfaceError):
            validate_u7_certificate(certificate)

    def test_equilibrium_outside_domain_fails(self):
        with self.assertRaises(U67InterfaceError):
            build_uniqueness_certificate(
                (1.2, 0.3, 0.4), 0.75,
                (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
                certified=True, provenance="U6"
            )

    def test_mismatched_dimensions_fail(self):
        with self.assertRaises(U67InterfaceError):
            build_uniqueness_certificate(
                (0.2, 0.3), 0.75,
                (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
                certified=True, provenance="U6"
            )

    def test_missing_provenance_fails(self):
        with self.assertRaises(U67InterfaceError):
            build_uniqueness_certificate(
                (0.2, 0.3, 0.4), 0.75,
                (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
                certified=True, provenance=""
            )


if __name__ == "__main__":
    unittest.main()
