from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:  # pragma: no cover - optional dependency
    spotipy = None
    SpotifyOAuth = None


@dataclass(frozen=True)
class PlaylistResult:
    name: str
    description: str
    tracks: list[dict[str, Any]]
    published: bool = False
    spotify_url: str | None = None


class PlaylistGenerator:
    def __init__(self) -> None:
        if load_dotenv is not None:
            load_dotenv()

        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.spotify_redirect_uri = os.getenv(
            "SPOTIFY_REDIRECT_URI",
            "http://localhost:8080/callback",
        )

    def generate(self, profile: dict, count: int = 12, publish_to_spotify: bool = False) -> PlaylistResult:
        name = self.generate_name(profile["moon_sign"], profile["moon_phase"])
        description = self.generate_description(profile)
        preview_tracks = self._generate_preview_tracks(profile, count)

        if publish_to_spotify:
            published = self._publish_to_spotify(name, description, profile, preview_tracks)
            if published is not None:
                return published

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

    def _publish_to_spotify(
        self,
        name: str,
        description: str,
        profile: dict,
        preview_tracks: list[dict[str, Any]],
    ) -> PlaylistResult | None:
        if not all([spotipy, SpotifyOAuth, self.spotify_client_id, self.spotify_client_secret]):
            return None

        spotify_client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri=self.spotify_redirect_uri,
                scope="playlist-modify-public",
            )
        )
        user_id = spotify_client.current_user()["id"]
        playlist = spotify_client.user_playlist_create(
            user=user_id,
            name=name,
            public=True,
            description=description,
        )

        uris = []
        for track in preview_tracks:
            result = spotify_client.search(q=track["search_hint"], type="track", limit=1)
            items = result.get("tracks", {}).get("items", [])
            if items:
                uris.append(items[0]["uri"])

        if uris:
            spotify_client.playlist_add_items(playlist["id"], uris)

        return PlaylistResult(
            name=name,
            description=description,
            tracks=preview_tracks,
            published=True,
            spotify_url=playlist["external_urls"]["spotify"],
        )
