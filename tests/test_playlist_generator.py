import unittest

from moontuner.mood_mapper import MoodMapper
from moontuner.playlist_generator import PlaylistGenerator


class PlaylistGeneratorTests(unittest.TestCase):
    def test_preview_playlist_is_deterministic(self) -> None:
        profile = MoodMapper().create_profile("Cancer", "waning_crescent")
        playlist = PlaylistGenerator().generate(profile, count=3)

        self.assertEqual(playlist.name, "Cancer Moon • Waning Crescent")
        self.assertEqual(len(playlist.tracks), 3)
        self.assertFalse(playlist.published)
        self.assertEqual(playlist.tracks[0]["artist"], "Lunar Current")
        self.assertEqual(playlist.tracks[0]["title"], "Cancer Indie Orbit 1")


if __name__ == "__main__":
    unittest.main()
