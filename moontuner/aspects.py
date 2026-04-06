"""Astrological aspect calculation between two ecliptic longitudes."""

from __future__ import annotations

from dataclasses import dataclass

# Major aspects: name -> (exact angle, default orb)
_ASPECT_DEFS: dict[str, tuple[float, float]] = {
    "conjunction": (0.0, 8.0),
    "sextile": (60.0, 6.0),
    "square": (90.0, 8.0),
    "trine": (120.0, 8.0),
    "opposition": (180.0, 8.0),
}

# How aspects to the natal moon modify the mood profile.
# Positive energy/valence delta = more energetic/positive.
_TRANSIT_MOON_MODIFIERS: dict[str, tuple[float, float, str]] = {
    "conjunction": (
        0.05,
        0.0,
        "Current moon conjunct natal moon: heightened emotional sensitivity",
    ),
    "sextile": (0.0, 0.05, "Current moon sextile natal moon: gentle emotional support"),
    "square": (0.10, -0.10, "Current moon square natal moon: emotional restlessness and tension"),
    "trine": (0.05, 0.10, "Current moon trine natal moon: emotional harmony and ease"),
    "opposition": (-0.05, -0.10, "Current moon opposite natal moon: inner tension and reflection"),
}


@dataclass(frozen=True)
class Aspect:
    """A detected astrological aspect between two points."""

    name: str
    exact_angle: float
    actual_angle: float
    orb: float
    intensity: float  # 1.0 = exact, 0.0 = at orb boundary
    energy_modifier: float
    valence_modifier: float
    description: str


def _angular_distance(lon_a: float, lon_b: float) -> float:
    """Return the shortest angular distance between two ecliptic longitudes (0-180)."""
    diff = abs(lon_a - lon_b) % 360
    return diff if diff <= 180 else 360 - diff


def compute_moon_aspects(
    natal_moon_longitude: float, transit_moon_longitude: float
) -> list[Aspect]:
    """Return all major aspects between the transit moon and the natal moon position.

    Parameters
    ----------
    natal_moon_longitude:
        Ecliptic longitude (0-360°) of the natal (birth) moon.
    transit_moon_longitude:
        Ecliptic longitude (0-360°) of the current (transit) moon.

    Returns
    -------
    list[Aspect]
        Active aspects sorted by intensity (tightest orb first).
    """
    actual_angle = _angular_distance(natal_moon_longitude, transit_moon_longitude)
    aspects: list[Aspect] = []

    for name, (exact_angle, max_orb) in _ASPECT_DEFS.items():
        orb = abs(actual_angle - exact_angle)
        if orb <= max_orb:
            intensity = 1.0 - (orb / max_orb)
            e_mod, v_mod, desc = _TRANSIT_MOON_MODIFIERS[name]
            aspects.append(
                Aspect(
                    name=name,
                    exact_angle=exact_angle,
                    actual_angle=actual_angle,
                    orb=round(orb, 2),
                    intensity=round(intensity, 3),
                    energy_modifier=e_mod,
                    valence_modifier=v_mod,
                    description=desc,
                )
            )

    aspects.sort(key=lambda a: -a.intensity)
    return aspects
