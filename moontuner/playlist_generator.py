from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import spotify_client as _spotify


@dataclass(frozen=True)
class PlaylistResult:
    name: str
    description: str
    tracks: list[dict[str, Any]]
    published: bool = False
    spotify_url: str | None = None


class PlaylistGenerator:
    def __init__(self) -> None:
        pass

    def generate(
        self, profile: dict, count: int = 12, publish_to_spotify: bool = False
    ) -> PlaylistResult:
        name = self.generate_name(profile["moon_sign"], profile["moon_phase"])
        description = self.generate_description(profile)

        # Attempt real Spotify-backed selection when requested and credentials exist.
        sp = _spotify.build_client() if publish_to_spotify else None

        if sp is not None:
            real_tracks = _spotify.select_tracks(sp, profile, count)
            if real_tracks:
                spotify_url: str | None = None
                if publish_to_spotify:
                    spotify_url = _spotify.publish_playlist(
                        sp, name, description, real_tracks, public=True
                    )
                return PlaylistResult(
                    name=name,
                    description=description,
                    tracks=real_tracks,
                    published=spotify_url is not None,
                    spotify_url=spotify_url,
                )

        # Offline fallback: deterministic preview tracks.
        preview_tracks = self._generate_preview_tracks(profile, count)
        return PlaylistResult(name=name, description=description, tracks=preview_tracks)

    @staticmethod
    def generate_name(moon_sign: str, moon_phase: str) -> str:
        return f"{moon_sign} Moon • {moon_phase.replace('_', ' ').title()}"

    @staticmethod
    def generate_description(profile: dict) -> str:
        return (
            f"{profile['phase_description']} playlist for a {profile['moon_sign']} moon: "
            f"{', '.join(profile['keywords'][:3])}; "
            f"energy {profile['target_energy']:.0%}; "
            f"mood {profile['target_valence']:.0%}."
        )

    def _generate_preview_tracks(self, profile: dict, count: int) -> list[dict[str, Any]]:
        tempo_min, tempo_max = profile["tempo_range"]
        tempo_step = 0 if count <= 1 else (tempo_max - tempo_min) / (count - 1)
        artists = {
            "fire": "Solar Echo",
            "earth": "Grounded Tides",
            "air": "Velvet Static",
            "water": "Lunar Current",
        }

        tracks = []
        for index in range(count):
            genre = profile["genres"][index % len(profile["genres"])]
            keyword = profile["keywords"][index % len(profile["keywords"])]
            tempo = round(tempo_min + (tempo_step * index))
            tracks.append(
                {
                    "title": f"{profile['moon_sign']} {genre.title()} Orbit {index + 1}",
                    "artist": artists[profile["element"]],
                    "genre": genre,
                    "keyword": keyword,
                    "tempo": tempo,
                    "search_hint": f'genre:"{genre}" {keyword} {tempo} BPM',
                }
            )

        return tracks
