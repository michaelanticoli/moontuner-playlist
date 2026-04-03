from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .aspects import Aspect


MOON_SIGN_PROFILES = {
    "Aries": {
        "element": "fire",
        "keywords": ["energetic", "impulsive", "pioneering", "bold"],
        "energy": 0.85,
        "valence": 0.75,
        "tempo_range": (120, 160),
        "danceability": 0.70,
        "acousticness": 0.20,
        "genres": ["rock", "electronic", "hip hop", "pop punk"],
    },
    "Taurus": {
        "element": "earth",
        "keywords": ["stable", "sensual", "grounded", "patient"],
        "energy": 0.40,
        "valence": 0.60,
        "tempo_range": (60, 100),
        "danceability": 0.50,
        "acousticness": 0.70,
        "genres": ["r&b", "soul", "jazz", "acoustic"],
    },
    "Gemini": {
        "element": "air",
        "keywords": ["curious", "communicative", "versatile", "witty"],
        "energy": 0.70,
        "valence": 0.80,
        "tempo_range": (100, 140),
        "danceability": 0.65,
        "acousticness": 0.30,
        "genres": ["pop", "indie pop", "electronic", "alternative"],
    },
    "Cancer": {
        "element": "water",
        "keywords": ["emotional", "nurturing", "intuitive", "nostalgic"],
        "energy": 0.35,
        "valence": 0.45,
        "tempo_range": (70, 110),
        "danceability": 0.40,
        "acousticness": 0.60,
        "genres": ["indie", "singer-songwriter", "ambient", "folk"],
    },
    "Leo": {
        "element": "fire",
        "keywords": ["dramatic", "confident", "creative", "passionate"],
        "energy": 0.80,
        "valence": 0.85,
        "tempo_range": (110, 150),
        "danceability": 0.75,
        "acousticness": 0.15,
        "genres": ["pop", "dance", "theatrical", "glam rock"],
    },
    "Virgo": {
        "element": "earth",
        "keywords": ["analytical", "practical", "perfectionist", "modest"],
        "energy": 0.50,
        "valence": 0.55,
        "tempo_range": (90, 120),
        "danceability": 0.45,
        "acousticness": 0.50,
        "genres": ["indie", "alternative", "folk", "chamber pop"],
    },
    "Libra": {
        "element": "air",
        "keywords": ["harmonious", "diplomatic", "aesthetic", "romantic"],
        "energy": 0.55,
        "valence": 0.70,
        "tempo_range": (80, 120),
        "danceability": 0.60,
        "acousticness": 0.40,
        "genres": ["pop", "r&b", "soft rock", "dream pop"],
    },
    "Scorpio": {
        "element": "water",
        "keywords": ["intense", "mysterious", "transformative", "passionate"],
        "energy": 0.65,
        "valence": 0.35,
        "tempo_range": (80, 130),
        "danceability": 0.55,
        "acousticness": 0.25,
        "genres": ["alternative", "darkwave", "trip hop", "gothic"],
    },
    "Sagittarius": {
        "element": "fire",
        "keywords": ["adventurous", "optimistic", "philosophical", "free"],
        "energy": 0.75,
        "valence": 0.80,
        "tempo_range": (100, 140),
        "danceability": 0.65,
        "acousticness": 0.35,
        "genres": ["world", "reggae", "folk rock", "indie rock"],
    },
    "Capricorn": {
        "element": "earth",
        "keywords": ["ambitious", "disciplined", "traditional", "responsible"],
        "energy": 0.60,
        "valence": 0.50,
        "tempo_range": (70, 110),
        "danceability": 0.40,
        "acousticness": 0.45,
        "genres": ["classical", "jazz", "blues", "classic rock"],
    },
    "Aquarius": {
        "element": "air",
        "keywords": ["innovative", "independent", "humanitarian", "eccentric"],
        "energy": 0.70,
        "valence": 0.65,
        "tempo_range": (90, 140),
        "danceability": 0.60,
        "acousticness": 0.20,
        "genres": ["electronic", "experimental", "synthpop", "future bass"],
    },
    "Pisces": {
        "element": "water",
        "keywords": ["dreamy", "compassionate", "artistic", "intuitive"],
        "energy": 0.40,
        "valence": 0.50,
        "tempo_range": (60, 100),
        "danceability": 0.35,
        "acousticness": 0.65,
        "genres": ["ambient", "dream pop", "shoegaze", "new age"],
    },
}

PHASE_MODIFIERS = {
    "new_moon": {
        "energy_modifier": -0.10,
        "valence_modifier": -0.05,
        "description": "Introspective and minimal",
    },
    "waxing_crescent": {
        "energy_modifier": 0.05,
        "valence_modifier": 0.05,
        "description": "Building energy",
    },
    "first_quarter": {
        "energy_modifier": 0.10,
        "valence_modifier": 0.05,
        "description": "Taking action",
    },
    "waxing_gibbous": {
        "energy_modifier": 0.15,
        "valence_modifier": 0.10,
        "description": "Refining and adjusting",
    },
    "full_moon": {
        "energy_modifier": 0.20,
        "valence_modifier": 0.10,
        "description": "Peak intensity",
    },
    "waning_gibbous": {
        "energy_modifier": 0.05,
        "valence_modifier": 0.00,
        "description": "Gratitude and sharing",
    },
    "last_quarter": {
        "energy_modifier": -0.05,
        "valence_modifier": -0.05,
        "description": "Release and letting go",
    },
    "waning_crescent": {
        "energy_modifier": -0.10,
        "valence_modifier": -0.10,
        "description": "Rest and renewal",
    },
}


class MoodMapper:
    def create_profile(self, moon_sign: str, moon_phase: str) -> dict:
        base = deepcopy(MOON_SIGN_PROFILES.get(moon_sign, MOON_SIGN_PROFILES["Cancer"]))
        phase = PHASE_MODIFIERS.get(moon_phase, PHASE_MODIFIERS["new_moon"])

        base["moon_sign"] = moon_sign if moon_sign in MOON_SIGN_PROFILES else "Cancer"
        base["moon_phase"] = moon_phase
        base["phase_description"] = phase["description"]
        base["target_energy"] = self._bounded(base["energy"] + phase["energy_modifier"])
        base["target_valence"] = self._bounded(base["valence"] + phase["valence_modifier"])

        return base

    def apply_transit_modifiers(self, profile: dict, aspects: list[Aspect]) -> dict:
        """Apply transit aspect modifiers to an existing profile in-place and return it."""
        for aspect in aspects:
            profile["target_energy"] = self._bounded(
                profile["target_energy"] + aspect.energy_modifier * aspect.intensity
            )
            profile["target_valence"] = self._bounded(
                profile["target_valence"] + aspect.valence_modifier * aspect.intensity
            )
        return profile

    @staticmethod
    def _bounded(value: float) -> float:
        return max(0.0, min(1.0, value))
