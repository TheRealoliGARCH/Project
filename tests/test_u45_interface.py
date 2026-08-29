import unittest

from src.u45_interface import CausalDesign, U45InterfaceError, build_causal_design, validate_causal_design


class TestU45Interface(unittest.TestCase):
    def design(self):
        return build_causal_design(
            (1.0, 0.0, 1.0),
            (2.0, 3.0, 4.0),
            (1.5, 2.5, 3.5),
            (2.5, 3.5, 4.5),
            scenario_id="stress-001",
            treatment_assigned_by_design=True,
            exogeneity_assumed=False,
            provenance="U4 deterministic stress harness",
            covariates=((0.2, 0.3, 0.4),),
        )

    def test_complete_design_validates(self):
        design = self.design()
        validate_causal_design(design)
        self.assertEqual(design.scenario_id, "stress-001")
        self.assertFalse(design.exogeneity_assumed)

    def test_stress_scenario_does_not_imply_exogeneity(self):
        design = self.design()
        self.assertTrue(design.treatment_assigned_by_design)
        self.assertFalse(design.exogeneity_assumed)

    def test_potential_outcomes_are_preserved(self):
        design = self.design()
        self.assertEqual(design.potential_outcome_0, (1.5, 2.5, 3.5))
        self.assertEqual(design.potential_outcome_1, (2.5, 3.5, 4.5))

    def test_missing_scenario_id_fails(self):
        with self.assertRaises(U45InterfaceError):
            build_causal_design(
                (1.0, 0.0, 1.0), (2.0, 3.0, 4.0), (1.0, 2.0, 3.0), (2.0, 3.0, 4.0),
                scenario_id="", treatment_assigned_by_design=True,
                exogeneity_assumed=False, provenance="U4"
            )

    def test_missing_provenance_fails(self):
        with self.assertRaises(U45InterfaceError):
            build_causal_design(
                (1.0, 0.0, 1.0), (2.0, 3.0, 4.0), (1.0, 2.0, 3.0), (2.0, 3.0, 4.0),
                scenario_id="s1", treatment_assigned_by_design=True,
                exogeneity_assumed=False, provenance=""
            )

    def test_wrong_dimension_fails(self):
        with self.assertRaises(U45InterfaceError):
            build_causal_design(
                (1.0, 0.0), (2.0, 3.0, 4.0), (1.0, 2.0, 3.0), (2.0, 3.0, 4.0),
                scenario_id="s1", treatment_assigned_by_design=True,
                exogeneity_assumed=False, provenance="U4"
            )

    def test_nonfinite_value_fails(self):
        with self.assertRaises(U45InterfaceError):
            build_causal_design(
                (1.0, float("nan"), 1.0), (2.0, 3.0, 4.0), (1.0, 2.0, 3.0), (2.0, 3.0, 4.0),
                scenario_id="s1", treatment_assigned_by_design=True,
                exogeneity_assumed=False, provenance="U4"
            )


if __name__ == "__main__":
    unittest.main()
