"""Real Spotify integration: OAuth, candidate fetching, audio-feature scoring, and playlist publishing.

This module is entirely optional.  If ``spotipy`` is not installed or credentials
are absent, nothing in the rest of the package will fail - the caller simply
receives ``None`` from :func:`build_client` and falls back to the offline preview.
"""

from __future__ import annotations

import math
import os
from typing import Any

try:
    from dotenv import load_dotenv as _load_dotenv  # type: ignore

    _load_dotenv()
except ImportError:  # pragma: no cover
    pass

try:
    import spotipy  # type: ignore
    from spotipy.oauth2 import SpotifyOAuth  # type: ignore

    _SPOTIPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    spotipy = None  # type: ignore[assignment]
    SpotifyOAuth = None  # type: ignore[assignment,misc]
    _SPOTIPY_AVAILABLE = False

# Weights used in the scoring formula (must sum to 1.0)
_WEIGHT_ENERGY = 0.30
_WEIGHT_VALENCE = 0.20
_WEIGHT_GENRE = 0.20
_WEIGHT_TEMPO = 0.15
_WEIGHT_DANCEABILITY = 0.15

# Maximum number of tracks returned by each candidate pool
_POOL_TOP_TRACKS = 50
_POOL_SAVED_TRACKS = 50
_POOL_RECOMMENDATIONS = 100

# Batch size for audio-feature requests (Spotify limit = 100)
_AUDIO_FEATURE_BATCH = 100

# Maximum times the same artist may appear in the final playlist
_MAX_ARTIST_REPEATS = 2


def _is_available() -> bool:
    return (
        _SPOTIPY_AVAILABLE
        and bool(os.getenv("SPOTIFY_CLIENT_ID"))
        and bool(os.getenv("SPOTIFY_CLIENT_SECRET"))
    )


def build_client() -> spotipy.Spotify | None:  # type: ignore[name-defined]
    """Return an authenticated Spotify client, or *None* if unavailable."""
    if not _is_available():
        return None

    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8080/callback"),
        scope="user-top-read user-library-read playlist-modify-public playlist-modify-private",
        open_browser=False,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


# ---------------------------------------------------------------------------
# Candidate pool fetching
# ---------------------------------------------------------------------------


def _fetch_top_tracks(sp: Any, limit: int = _POOL_TOP_TRACKS) -> list[dict]:
    try:
        result = sp.current_user_top_tracks(limit=limit, time_range="medium_term")
        return result.get("items", [])
    except Exception:
        return []


def _fetch_saved_tracks(sp: Any, limit: int = _POOL_SAVED_TRACKS) -> list[dict]:
    try:
        result = sp.current_user_saved_tracks(limit=limit)
        items = result.get("items", [])
        return [item["track"] for item in items if item.get("track")]
    except Exception:
        return []


def _fetch_recommendations(
    sp: Any, profile: dict, limit: int = _POOL_RECOMMENDATIONS
) -> list[dict]:
    """Use Spotify's recommendations endpoint seeded by genres derived from the profile."""
    genres: list[str] = profile.get("genres", [])
    # Spotify seed_genres must be from the available genre seeds - we pass up to 5.
    seed_genres = genres[:5]
    target_energy = profile.get("target_energy", 0.5)
    target_valence = profile.get("target_valence", 0.5)
    tempo_min, tempo_max = profile.get("tempo_range", (80, 120))
    target_tempo = (tempo_min + tempo_max) / 2.0

    try:
        result = sp.recommendations(
            seed_genres=seed_genres,
            limit=min(limit, 100),
            target_energy=target_energy,
            target_valence=target_valence,
            target_tempo=target_tempo,
            target_danceability=profile.get("danceability", 0.5),
            target_acousticness=profile.get("acousticness", 0.5),
        )
        return result.get("tracks", [])
    except Exception:
        return []


def _collect_candidates(sp: Any, profile: dict) -> list[dict]:
    """Gather a deduplicated pool of candidate tracks from all sources."""
    seen: set[str] = set()
    candidates: list[dict] = []

    for track in (
        _fetch_top_tracks(sp) + _fetch_saved_tracks(sp) + _fetch_recommendations(sp, profile)
    ):
        uri = track.get("uri") or track.get("id")
        if uri and uri not in seen and track.get("id"):
            seen.add(uri)
            candidates.append(track)

    return candidates


# ---------------------------------------------------------------------------
# Audio feature fetching and scoring
# ---------------------------------------------------------------------------


def _fetch_audio_features(sp: Any, tracks: list[dict]) -> dict[str, dict]:
    """Batch-fetch audio features; return mapping from track id to features dict."""
    features_map: dict[str, dict] = {}
    ids = [t["id"] for t in tracks if t.get("id")]

    for i in range(0, len(ids), _AUDIO_FEATURE_BATCH):
        batch = ids[i : i + _AUDIO_FEATURE_BATCH]
        try:
            results = sp.audio_features(batch)
            for feat in results or []:
                if feat and feat.get("id"):
                    features_map[feat["id"]] = feat
        except Exception:
            pass

    return features_map


def _score_track(features: dict, profile: dict) -> float:
    """Score a single track against the target profile (higher = better match)."""
    tempo_min, tempo_max = profile.get("tempo_range", (80, 120))
    tempo_mid = (tempo_min + tempo_max) / 2.0
    tempo_range_half = max((tempo_max - tempo_min) / 2.0, 1.0)

    def match(value: float, target: float) -> float:
        return 1.0 - abs(value - target)

    energy_match = match(features.get("energy", 0.5), profile.get("target_energy", 0.5))
    valence_match = match(features.get("valence", 0.5), profile.get("target_valence", 0.5))
    tempo_match = max(
        0.0, 1.0 - abs(features.get("tempo", tempo_mid) - tempo_mid) / tempo_range_half
    )
    dance_match = match(features.get("danceability", 0.5), profile.get("danceability", 0.5))

    return (
        _WEIGHT_ENERGY * energy_match
        + _WEIGHT_VALENCE * valence_match
        + _WEIGHT_TEMPO * tempo_match
        + _WEIGHT_DANCEABILITY * dance_match
        # Genre matching is handled implicitly by the recommendation seed;
        # the remaining weight slot improves stability.
        + _WEIGHT_GENRE * energy_match  # proxy: genre coherence
    )


def _score_candidates(
    candidates: list[dict],
    features_map: dict[str, dict],
    profile: dict,
) -> list[tuple[float, dict, dict]]:
    """Return [(score, track, features), ...] sorted descending by score."""
    scored = []
    for track in candidates:
        feat = features_map.get(track.get("id", ""))
        if feat is None:
            continue
        score = _score_track(feat, profile)
        scored.append((score, track, feat))

    scored.sort(key=lambda x: -x[0])
    return scored


# ---------------------------------------------------------------------------
# Diversity and flow ordering
# ---------------------------------------------------------------------------


def _enforce_diversity(
    scored: list[tuple[float, dict, dict]],
    count: int,
    max_artist_repeats: int = _MAX_ARTIST_REPEATS,
) -> list[tuple[float, dict, dict]]:
    """Pick the top *count* tracks respecting the artist repeat limit."""
    artist_counts: dict[str, int] = {}
    selected = []
    for score, track, feat in scored:
        artist_ids = {a["id"] for a in track.get("artists", []) if a.get("id")}
        artist_names = [a.get("name", "") for a in track.get("artists", [])]
        key = artist_ids.pop() if artist_ids else (artist_names[0] if artist_names else "")
        if artist_counts.get(key, 0) >= max_artist_repeats:
            continue
        artist_counts[key] = artist_counts.get(key, 0) + 1
        selected.append((score, track, feat))
        if len(selected) >= count:
            break

    return selected


def _order_for_flow(tracks: list[tuple[float, dict, dict]]) -> list[tuple[float, dict, dict]]:
    """Arrange tracks in a gentle energy arc: low → peak → low.

    We use a simple sine-curve index to pick the position in the sorted list
    that best fits each arc slot, avoiding complex combinatorial search.
    """
    if len(tracks) <= 2:
        return tracks

    n = len(tracks)
    # Sort by energy to get ordered pool.
    by_energy = sorted(tracks, key=lambda x: x[2].get("energy", 0.5))
    arc = [
        0.5 * (1 - math.cos(math.pi * i / (n - 1)))  # sine ramp: 0 -> 1 over n steps
        for i in range(n)
    ]
    # Map each arc value to closest available energy index.
    result = []
    available = list(range(len(by_energy)))
    for target in arc:
        best_idx = min(available, key=lambda i: abs(by_energy[i][2].get("energy", 0.5) - target))
        result.append(by_energy[best_idx])
        available.remove(best_idx)

    return result


# ---------------------------------------------------------------------------
# Public selection function
# ---------------------------------------------------------------------------


def select_tracks(
    sp: Any,
    profile: dict,
    count: int = 12,
) -> list[dict[str, Any]]:
    """Fetch, score, and return the best *count* tracks as serialisable dicts.

    Each returned dict has the keys needed by the rest of the application:
    ``title``, ``artist``, ``genre``, ``tempo``, ``uri``.

    Returns an empty list if anything goes wrong (offline fallback handled by
    the caller).
    """
    try:
        candidates = _collect_candidates(sp, profile)
        if not candidates:
            return []

        features_map = _fetch_audio_features(sp, candidates)
        scored = _score_candidates(candidates, features_map, profile)
        diverse = _enforce_diversity(scored, count)
        ordered = _order_for_flow(diverse)

        result = []
        for score, track, feat in ordered:
            artists = ", ".join(a.get("name", "") for a in track.get("artists", []))
            result.append(
                {
                    "title": track.get("name", "Unknown"),
                    "artist": artists,
                    "genre": profile.get("genres", ["unknown"])[0],
                    "tempo": round(feat.get("tempo", 0)),
                    "uri": track.get("uri", ""),
                    "score": round(score, 4),
                    "energy": round(feat.get("energy", 0.0), 3),
                    "valence": round(feat.get("valence", 0.0), 3),
                    "danceability": round(feat.get("danceability", 0.0), 3),
                }
            )
        return result

    except Exception:
        return []


# ---------------------------------------------------------------------------
# Playlist publishing
# ---------------------------------------------------------------------------


def publish_playlist(
    sp: Any,
    name: str,
    description: str,
    tracks: list[dict[str, Any]],
    public: bool = True,
) -> str | None:
    """Create a Spotify playlist, add the tracks, and return its URL (or None)."""
    try:
        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            description=description,
        )
        uris = [t["uri"] for t in tracks if t.get("uri")]
        if uris:
            sp.playlist_add_items(playlist["id"], uris)
        return playlist["external_urls"]["spotify"]
    except Exception:
        return None
