"""Tests for Spotify client scoring helpers (no real Spotify credentials needed)."""

import unittest

from moontuner.spotify_client import (
    _enforce_diversity,
    _order_for_flow,
    _score_track,
)


def _make_features(**kwargs: float) -> dict:
    defaults = {
        "energy": 0.5,
        "valence": 0.5,
        "tempo": 100.0,
        "danceability": 0.5,
        "acousticness": 0.5,
    }
    defaults.update(kwargs)
    return defaults


def _make_scored_entry(score: float, track: dict, feat: dict) -> tuple:
    return (score, track, feat)


class TrackScoringTests(unittest.TestCase):
    def _profile(self, **overrides: object) -> dict:
        base: dict = {
            "target_energy": 0.8,
            "target_valence": 0.7,
            "tempo_range": (100, 140),
            "danceability": 0.7,
            "acousticness": 0.2,
            "genres": ["pop"],
        }
        base.update(overrides)
        return base

    def test_perfect_match_scores_near_one(self) -> None:
        profile = self._profile(target_energy=0.8, target_valence=0.7)
        features = _make_features(energy=0.8, valence=0.7, tempo=120.0, danceability=0.7)

        score = _score_track(features, profile)
        self.assertGreater(score, 0.85)

    def test_poor_match_scores_below_good_match(self) -> None:
        profile = self._profile(target_energy=0.8, target_valence=0.7)
        good_features = _make_features(energy=0.8, valence=0.7, tempo=120.0, danceability=0.7)
        poor_features = _make_features(energy=0.1, valence=0.1, tempo=60.0, danceability=0.1)

        good_score = _score_track(good_features, profile)
        poor_score = _score_track(poor_features, profile)
        self.assertGreater(good_score, poor_score)

    def test_score_bounded_0_to_1(self) -> None:
        profile = self._profile()
        for energy in [0.0, 0.5, 1.0]:
            for valence in [0.0, 0.5, 1.0]:
                score = _score_track(_make_features(energy=energy, valence=valence), profile)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0 + 1e-9)


class DiversityTests(unittest.TestCase):
    def _make_track(self, artist_id: str) -> dict:
        return {
            "id": f"track_{artist_id}",
            "name": "Track",
            "artists": [{"id": artist_id, "name": artist_id}],
        }

    def test_artist_repeat_limit_enforced(self) -> None:
        # 4 entries from artist "A" → only 2 should survive.
        scored = [
            (0.9, self._make_track("A"), _make_features()),
            (0.88, self._make_track("A"), _make_features()),
            (0.85, self._make_track("A"), _make_features()),
            (0.80, self._make_track("A"), _make_features()),
        ]
        result = _enforce_diversity(scored, count=4, max_artist_repeats=2)

        self.assertEqual(len(result), 2)

    def test_count_respected(self) -> None:
        scored = [
            (0.9 - i * 0.01, self._make_track(f"artist_{i}"), _make_features()) for i in range(20)
        ]
        result = _enforce_diversity(scored, count=5)

        self.assertEqual(len(result), 5)


class FlowOrderingTests(unittest.TestCase):
    def _entry(self, energy: float) -> tuple:
        return (
            0.5,
            {"id": f"t_{energy}", "name": "T", "artists": []},
            _make_features(energy=energy),
        )

    def test_single_track_unchanged(self) -> None:
        tracks = [self._entry(0.5)]
        result = _order_for_flow(tracks)
        self.assertEqual(len(result), 1)

    def test_output_length_preserved(self) -> None:
        tracks = [self._entry(e) for e in [0.2, 0.8, 0.5, 0.9, 0.1]]
        result = _order_for_flow(tracks)
        self.assertEqual(len(result), len(tracks))

    def test_all_input_entries_present_in_output(self) -> None:
        tracks = [self._entry(e) for e in [0.2, 0.8, 0.5, 0.9, 0.1]]
        result = _order_for_flow(tracks)
        input_ids = {t[1]["id"] for t in tracks}
        output_ids = {t[1]["id"] for t in result}
        self.assertEqual(input_ids, output_ids)


if __name__ == "__main__":
    unittest.main()
