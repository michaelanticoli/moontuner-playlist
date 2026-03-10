import unittest

from moontuner.moon_calculator import MOON_SIGNS, PHASE_NAMES, MoonCalculator


class MoonCalculatorTests(unittest.TestCase):
    def test_calculate_returns_valid_reading(self) -> None:
        reading = MoonCalculator(use_swisseph=False).calculate("1990-07-15", "14:30")

        self.assertIn(reading.moon_sign, MOON_SIGNS)
        self.assertIn(reading.moon_phase, PHASE_NAMES)
        self.assertGreaterEqual(reading.illuminated_fraction, 0.0)
        self.assertLessEqual(reading.illuminated_fraction, 1.0)
        self.assertEqual(reading.source, "approximation")


if __name__ == "__main__":
    unittest.main()
