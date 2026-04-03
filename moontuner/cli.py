from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from .aspects import compute_moon_aspects
from .mood_mapper import MoodMapper
from .moon_calculator import MoonCalculator
from .playlist_generator import PlaylistGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a moon-sign playlist from birth data.",
    )
    parser.add_argument(
        "--birth-date", default="1990-07-15", help="Birth date in YYYY-MM-DD format."
    )
    parser.add_argument("--birth-time", default="14:30", help="Birth time in HH:MM format.")
    parser.add_argument("--lat", type=float, default=None, help="Optional birth latitude.")
    parser.add_argument("--lon", type=float, default=None, help="Optional birth longitude.")
    parser.add_argument("--moon-sign", help="Override the calculated moon sign.")
    parser.add_argument("--phase", help="Override the calculated moon phase.")
    parser.add_argument(
        "--count", type=int, default=12, help="Number of playlist entries to generate."
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help=(
            "Date/time to use for transit calculation in YYYY-MM-DD or YYYY-MM-DD HH:MM format. "
            "Defaults to now."
        ),
    )
    parser.add_argument(
        "--publish-spotify",
        action="store_true",
        help="Publish the generated playlist to Spotify when credentials and spotipy are available.",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print a human-readable explanation of the astrological reasoning.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output the result as JSON instead of plain text.",
    )
    return parser


def _parse_as_of(as_of: str | None) -> datetime:
    if as_of is None:
        return datetime.now()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(as_of, fmt)
        except ValueError:
            continue
    raise SystemExit(
        f'--as-of value {as_of!r} must be in YYYY-MM-DD or "YYYY-MM-DD HH:MM" format (24-hour time).'
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    moon_calculator = MoonCalculator()
    mood_mapper = MoodMapper()
    playlist_generator = PlaylistGenerator()

    # Natal moon reading (from birth data).
    natal_reading = moon_calculator.calculate(
        birth_date=args.birth_date,
        birth_time=args.birth_time,
        latitude=args.lat,
        longitude=args.lon,
    )
    moon_sign = args.moon_sign or natal_reading.moon_sign
    moon_phase = args.phase or natal_reading.moon_phase

    # Transit moon reading (current or --as-of time).
    transit_moment = _parse_as_of(args.as_of)
    transit_reading = moon_calculator.calculate(
        birth_date=transit_moment.date(),
        birth_time=transit_moment.time(),
    )

    # Compute aspects between transit moon and natal moon.
    aspects = compute_moon_aspects(natal_reading.moon_longitude, transit_reading.moon_longitude)

    # Build profile and apply transit modifiers.
    profile = mood_mapper.create_profile(moon_sign, moon_phase)
    if aspects:
        mood_mapper.apply_transit_modifiers(profile, aspects)

    playlist = playlist_generator.generate(
        profile=profile,
        count=max(1, args.count),
        publish_to_spotify=args.publish_spotify,
    )

    if args.output_json:
        output = {
            "astrology": {
                "natal_moon_sign": moon_sign,
                "natal_moon_degree": round(natal_reading.moon_degree_within_sign, 2),
                "natal_moon_longitude": round(natal_reading.moon_longitude, 2),
                "moon_phase": moon_phase,
                "source": natal_reading.source,
                "transit_moon_sign": transit_reading.moon_sign,
                "transit_moon_longitude": round(transit_reading.moon_longitude, 2),
                "aspects": [
                    {
                        "name": a.name,
                        "orb": a.orb,
                        "intensity": a.intensity,
                        "description": a.description,
                    }
                    for a in aspects
                ],
            },
            "profile": {
                "target_energy": round(profile["target_energy"], 3),
                "target_valence": round(profile["target_valence"], 3),
                "genres": profile["genres"],
            },
            "playlist": {
                "name": playlist.name,
                "description": playlist.description,
                "published": playlist.published,
                "spotify_url": playlist.spotify_url,
                "tracks": playlist.tracks,
            },
        }
        print(json.dumps(output, indent=2))
        return 0

    print("🌙 MoonTuner Playlist Generator")
    print(
        f"Natal moon: {moon_sign} {natal_reading.moon_degree_within_sign:.1f}° ({natal_reading.source})"
    )
    print(f"Moon phase: {moon_phase.replace('_', ' ')}")
    print(
        f"Transit moon: {transit_reading.moon_sign} {transit_reading.moon_degree_within_sign:.1f}°"
    )
    print(f"Energy target: {profile['target_energy']:.2f}")
    print(f"Mood target: {profile['target_valence']:.2f}")
    print(f"Genres: {', '.join(profile['genres'])}")
    print(f"Playlist: {playlist.name}")
    print(playlist.description)

    if args.explain:
        print()
        print("── Astrological Explanation ──────────────────────────")
        print(
            f"  Natal moon in {moon_sign} at {natal_reading.moon_degree_within_sign:.1f}° "
            f"(longitude {natal_reading.moon_longitude:.1f}°)"
        )
        print(f"  {moon_sign} is a {profile['element']} sign: {', '.join(profile['keywords'])}")
        print(f"  Phase '{moon_phase.replace('_', ' ')}': {profile['phase_description']}")
        if aspects:
            print("  Active transit aspects to natal moon:")
            for aspect in aspects:
                print(
                    f"    • {aspect.name.title()} (orb {aspect.orb:.1f}°, intensity {aspect.intensity:.0%}): "
                    f"{aspect.description}"
                )
        else:
            print("  No major transit aspects to natal moon at this time.")
        print(
            f"  Final targets — energy: {profile['target_energy']:.2f}, "
            f"valence: {profile['target_valence']:.2f}"
        )
        print("──────────────────────────────────────────────────────")

    print()
    for index, track in enumerate(playlist.tracks, start=1):
        line = f"{index:02d}. {track['title']} — {track['artist']} [{track['genre']}, {track['tempo']} BPM]"
        if track.get("score") is not None:
            line += f" (score {track['score']:.3f})"
        print(line)

    if playlist.spotify_url:
        print()
        print(f"Spotify URL: {playlist.spotify_url}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
