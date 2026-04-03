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

    def test_reading_includes_longitude_and_degree(self) -> None:
        reading = MoonCalculator(use_swisseph=False).calculate("1990-07-15", "14:30")

        self.assertGreaterEqual(reading.moon_longitude, 0.0)
        self.assertLess(reading.moon_longitude, 360.0)
        self.assertGreaterEqual(reading.moon_degree_within_sign, 0.0)
        self.assertLess(reading.moon_degree_within_sign, 30.0)

    def test_degree_within_sign_consistent_with_longitude(self) -> None:
        reading = MoonCalculator(use_swisseph=False).calculate("2000-01-01", "00:00")

        expected_degree = reading.moon_longitude % 30
        self.assertAlmostEqual(reading.moon_degree_within_sign, expected_degree, places=10)

    def test_different_dates_produce_different_longitudes(self) -> None:
        r1 = MoonCalculator(use_swisseph=False).calculate("2020-01-01", "12:00")
        r2 = MoonCalculator(use_swisseph=False).calculate("2020-01-15", "12:00")
        self.assertNotAlmostEqual(r1.moon_longitude, r2.moon_longitude, places=1)


if __name__ == "__main__":
    unittest.main()
