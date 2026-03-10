from __future__ import annotations

import argparse

from .moon_calculator import MoonCalculator
from .mood_mapper import MoodMapper
from .playlist_generator import PlaylistGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a moon-sign playlist blueprint from birth data.",
    )
    parser.add_argument("--birth-date", default="1990-07-15", help="Birth date in YYYY-MM-DD format.")
    parser.add_argument("--birth-time", default="14:30", help="Birth time in HH:MM format.")
    parser.add_argument("--lat", type=float, default=None, help="Optional birth latitude.")
    parser.add_argument("--lon", type=float, default=None, help="Optional birth longitude.")
    parser.add_argument("--moon-sign", help="Override the calculated moon sign.")
    parser.add_argument("--phase", help="Override the calculated moon phase.")
    parser.add_argument("--count", type=int, default=12, help="Number of playlist entries to generate.")
    parser.add_argument(
        "--publish-spotify",
        action="store_true",
        help="Publish the generated playlist to Spotify when credentials and spotipy are available.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    moon_calculator = MoonCalculator()
    mood_mapper = MoodMapper()
    playlist_generator = PlaylistGenerator()

    reading = moon_calculator.calculate(
        birth_date=args.birth_date,
        birth_time=args.birth_time,
        latitude=args.lat,
        longitude=args.lon,
    )
    moon_sign = args.moon_sign or reading.moon_sign
    moon_phase = args.phase or reading.moon_phase

    profile = mood_mapper.create_profile(moon_sign, moon_phase)
    playlist = playlist_generator.generate(
        profile=profile,
        count=max(1, args.count),
        publish_to_spotify=args.publish_spotify,
    )

    print("🌙 MoonTuner Playlist Generator")
    print(f"Moon sign: {moon_sign} ({reading.source})")
    print(f"Moon phase: {moon_phase.replace('_', ' ')}")
    print(f"Energy target: {profile['target_energy']:.2f}")
    print(f"Mood target: {profile['target_valence']:.2f}")
    print(f"Genres: {', '.join(profile['genres'])}")
    print(f"Playlist: {playlist.name}")
    print(playlist.description)
    print()

    for index, track in enumerate(playlist.tracks, start=1):
        print(
            f"{index:02d}. {track['title']} — {track['artist']} "
            f"[{track['genre']}, {track['tempo']} BPM]"
        )

    if playlist.spotify_url:
        print()
        print(f"Spotify URL: {playlist.spotify_url}")

    return 0
