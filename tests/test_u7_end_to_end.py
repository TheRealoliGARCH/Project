import unittest

from src.u7_end_to_end import assert_deterministic, run_pipeline, stable_digest


def increment(state):
    return dict(state, value=state["value"] + 1)


def double(state):
    return dict(state, value=2 * state["value"])


def valid(state):
    return isinstance(state, dict) and isinstance(state.get("value"), int)


class TestU7EndToEnd(unittest.TestCase):
    def setUp(self):
        self.stages = (("U1", increment, valid), ("U2", double, valid))

    def test_pipeline_composes_stages(self):
        result = run_pipeline(self.stages, {"value": 1})
        self.assertEqual(result.outputs["U1"]["value"], 2)
        self.assertEqual(result.outputs["U2"]["value"], 4)
        self.assertEqual(len(result.digest), 64)

    def test_deterministic_reconstruction(self):
        result = assert_deterministic(self.stages, {"value": 1})
        self.assertEqual(result.outputs["U2"]["value"], 4)

    def test_stage_contract_failure(self):
        bad = (("U1", increment, lambda _: False),)
        with self.assertRaises(ValueError):
            run_pipeline(bad, {"value": 1})

    def test_empty_pipeline_rejected(self):
        with self.assertRaises(ValueError):
            run_pipeline((), {"value": 1})

    def test_digest_is_order_sensitive_for_stage_outputs(self):
        self.assertNotEqual(stable_digest({"a": 1, "b": 2}), stable_digest({"a": 1, "b": 3}))


if __name__ == "__main__":
    unittest.main()
