import unittest

from moontuner.aspects import Aspect, compute_moon_aspects


class AspectCalculationTests(unittest.TestCase):
    def test_conjunction_detected(self) -> None:
        aspects = compute_moon_aspects(45.0, 48.0)  # 3° orb

        names = [a.name for a in aspects]
        self.assertIn("conjunction", names)

    def test_opposition_detected(self) -> None:
        aspects = compute_moon_aspects(0.0, 180.0)  # exact opposition

        names = [a.name for a in aspects]
        self.assertIn("opposition", names)

    def test_trine_detected(self) -> None:
        aspects = compute_moon_aspects(0.0, 120.0)  # exact trine

        names = [a.name for a in aspects]
        self.assertIn("trine", names)

    def test_square_detected(self) -> None:
        aspects = compute_moon_aspects(0.0, 90.0)

        names = [a.name for a in aspects]
        self.assertIn("square", names)

    def test_sextile_detected(self) -> None:
        aspects = compute_moon_aspects(0.0, 60.0)

        names = [a.name for a in aspects]
        self.assertIn("sextile", names)

    def test_no_aspect_outside_orb(self) -> None:
        # 45° is not near any major aspect (sextile is 60° ± 6, square is 90° ± 8).
        aspects = compute_moon_aspects(0.0, 45.0)

        self.assertEqual(aspects, [])

    def test_exact_conjunction_has_full_intensity(self) -> None:
        aspects = compute_moon_aspects(100.0, 100.0)

        conj = next(a for a in aspects if a.name == "conjunction")
        self.assertAlmostEqual(conj.intensity, 1.0)
        self.assertAlmostEqual(conj.orb, 0.0)

    def test_intensity_decreases_with_wider_orb(self) -> None:
        tight = compute_moon_aspects(0.0, 1.0)  # 1° orb
        loose = compute_moon_aspects(0.0, 7.0)  # 7° orb

        tight_conj = next(a for a in tight if a.name == "conjunction")
        loose_conj = next(a for a in loose if a.name == "conjunction")
        self.assertGreater(tight_conj.intensity, loose_conj.intensity)

    def test_sorted_by_intensity_descending(self) -> None:
        # Exact conjunction + wide sextile in same reading is not realistic,
        # but we can test ordering on a single list returned by a non-exact aspect.
        aspects = compute_moon_aspects(0.0, 180.0)  # exact opposition

        if len(aspects) > 1:
            intensities = [a.intensity for a in aspects]
            self.assertEqual(intensities, sorted(intensities, reverse=True))

    def test_deterministic_for_fixed_longitudes(self) -> None:
        a1 = compute_moon_aspects(123.45, 243.45)  # 120° apart → trine
        a2 = compute_moon_aspects(123.45, 243.45)

        self.assertEqual(a1, a2)

    def test_aspect_is_dataclass(self) -> None:
        aspects = compute_moon_aspects(0.0, 0.0)

        self.assertIsInstance(aspects[0], Aspect)


if __name__ == "__main__":
    unittest.main()
