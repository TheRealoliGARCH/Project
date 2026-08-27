import unittest
from src.transform import benchmark_yield_as_continuous_decimal, transform_yields


class TransformTests(unittest.TestCase):
    def test_identity_on_decimal_yields(self):
        self.assertAlmostEqual(benchmark_yield_as_continuous_decimal(0.0329), 0.0329)
        self.assertEqual(transform_yields([0.01, 0.02]), [0.01, 0.02])

    def test_invalid_yield_rejected(self):
        with self.assertRaises(ValueError):
            benchmark_yield_as_continuous_decimal(-1.0)


if __name__ == "__main__":
    unittest.main()
