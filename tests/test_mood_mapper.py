import unittest

from moontuner.mood_mapper import MoodMapper


class MoodMapperTests(unittest.TestCase):
    def test_full_moon_profile_caps_energy(self) -> None:
        profile = MoodMapper().create_profile("Aries", "full_moon")

        self.assertEqual(profile["moon_sign"], "Aries")
        self.assertEqual(profile["moon_phase"], "full_moon")
        self.assertEqual(profile["target_energy"], 1.0)
        self.assertAlmostEqual(profile["target_valence"], 0.85)
        self.assertIn("rock", profile["genres"])


if __name__ == "__main__":
    unittest.main()
