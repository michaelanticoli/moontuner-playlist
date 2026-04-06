# Astrological Moon Sign Playlist Generation Algorithm

## Overview

This document describes the actual algorithm implemented in the MoonTuner codebase.
Where illustrative code snippets appear, they reflect the real module structure; the
canonical source of truth is always the Python source in `moontuner/`.

---

## Core Components

### 1. Astrological Data Collection (`moontuner/moon_calculator.py`)

#### 1.1 Natal Moon Sign Determination

`MoonCalculator.calculate()` accepts a birth date, birth time, and optional
latitude/longitude and returns a `MoonReading` dataclass:

```python
@dataclass(frozen=True)
class MoonReading:
    moon_sign: str               # e.g. "Aries"
    moon_phase: str              # e.g. "full_moon"
    illuminated_fraction: float  # 0.0-1.0
    source: str                  # "swisseph" | "approximation"
    moon_longitude: float        # ecliptic longitude 0-360 degrees
    moon_degree_within_sign: float  # 0-30 degrees within the sign
```

Two calculation paths are supported:

| Path | When used | Accuracy |
|---|---|---|
| Swiss Ephemeris (`pyswisseph`) | when installed | professional-grade |
| Built-in approximation | always available | +/-1-2 degrees typical error |

#### 1.2 Transit Moon Analysis

The same `MoonCalculator` is used a second time with the **current date/time**
(or a user-supplied `--as-of` timestamp) to obtain the transit moon longitude.

---

### 2. Aspect Calculation (`moontuner/aspects.py`)

Major aspects between the transit moon and the natal moon are detected and
returned as `Aspect` dataclass instances:

```python
@dataclass(frozen=True)
class Aspect:
    name: str           # "conjunction" | "sextile" | "square" | "trine" | "opposition"
    exact_angle: float  # 0, 60, 90, 120, or 180 degrees
    actual_angle: float # measured angular distance
    orb: float          # deviation from exact, in degrees
    intensity: float    # 1.0 = exact aspect, 0.0 = at orb boundary
    energy_modifier: float  # delta applied to target_energy
    valence_modifier: float # delta applied to target_valence
    description: str    # human-readable interpretation
```

**Supported aspects and default orbs:**

| Aspect | Exact angle | Default orb |
|---|---|---|
| Conjunction | 0 degrees | +/-8 degrees |
| Sextile | 60 degrees | +/-6 degrees |
| Square | 90 degrees | +/-8 degrees |
| Trine | 120 degrees | +/-8 degrees |
| Opposition | 180 degrees | +/-8 degrees |

**Transit moon to natal moon modifiers:**

| Aspect | Energy delta | Valence delta | Interpretation |
|---|---|---|---|
| Conjunction | +0.05 | 0.00 | Heightened emotional sensitivity |
| Sextile | 0.00 | +0.05 | Gentle emotional support |
| Square | +0.10 | -0.10 | Emotional restlessness and tension |
| Trine | +0.05 | +0.10 | Emotional harmony and ease |
| Opposition | -0.05 | -0.10 | Inner tension and reflection |

Each modifier is scaled by the aspect's `intensity` before being applied.

---

### 3. Mood Mapping (`moontuner/mood_mapper.py`)

#### 3.1 Moon Sign Profiles

`MOON_SIGN_PROFILES` is a fully implemented dictionary covering all 12 signs.
Each entry has the following schema:

```python
{
    "element": str,          # "fire" | "earth" | "air" | "water"
    "keywords": list[str],   # 4 adjectives describing the emotional tone
    "energy": float,         # base energy 0.0-1.0
    "valence": float,        # base valence (positivity) 0.0-1.0
    "tempo_range": tuple,    # (min_bpm, max_bpm)
    "danceability": float,   # 0.0-1.0
    "acousticness": float,   # 0.0-1.0
    "genres": list[str],     # 4 genre tags
}
```

All 12 sign profiles (Aries through Pisces) are defined in the source - see
[`moontuner/mood_mapper.py`](moontuner/mood_mapper.py) for the complete dataset.

#### 3.2 Phase Modifiers

`PHASE_MODIFIERS` contains energy and valence deltas for all 8 lunar phases:

| Phase | Energy delta | Valence delta | Description |
|---|---|---|---|
| new_moon | -0.10 | -0.05 | Introspective and minimal |
| waxing_crescent | +0.05 | +0.05 | Building energy |
| first_quarter | +0.10 | +0.05 | Taking action |
| waxing_gibbous | +0.15 | +0.10 | Refining and adjusting |
| full_moon | +0.20 | +0.10 | Peak intensity |
| waning_gibbous | +0.05 | 0.00 | Gratitude and sharing |
| last_quarter | -0.05 | -0.05 | Release and letting go |
| waning_crescent | -0.10 | -0.10 | Rest and renewal |

#### 3.3 Profile Creation and Transit Modification

```python
# 1. Build base profile from sign + phase:
profile = MoodMapper().create_profile(moon_sign, moon_phase)

# 2. Compute transit aspects:
aspects = compute_moon_aspects(natal_moon_longitude, transit_moon_longitude)

# 3. Apply aspect modifiers (each scaled by intensity):
MoodMapper().apply_transit_modifiers(profile, aspects)
```

The final `profile` dict contains `target_energy` and `target_valence` bounded
to `[0.0, 1.0]`.

---

### 4. Playlist Generation (`moontuner/playlist_generator.py`, `moontuner/spotify_client.py`)

#### 4.1 Spotify-Backed Selection (when credentials are present)

```
Candidate pool
  +-- user top tracks        (up to 50 via /me/top/tracks)
  +-- user saved tracks      (up to 50 via /me/tracks)
  +-- Spotify recommendations (up to 100, seeded by genres + target features)
          |
          v
  Deduplicate by URI
          |
          v
  Batch-fetch audio features (/audio-features, batches of 100)
          |
          v
  Score each track:
      score = 0.30 x energy_match
            + 0.20 x valence_match
            + 0.20 x genre_proxy      (energy coherence)
            + 0.15 x tempo_match
            + 0.15 x danceability_match
          |
          v
  Sort descending by score
          |
          v
  Enforce diversity (max 2 repeats per artist)
          |
          v
  Order for flow (sine-curve energy arc: low -> peak -> low)
          |
          v
  Publish playlist + add real track URIs
```

#### 4.2 Offline Fallback (no Spotify)

When `spotipy` is not installed or credentials are absent, `PlaylistGenerator`
falls back to deterministic preview tracks - themed by sign, genre, and tempo -
so the CLI always produces output.

---

### 5. Implementation Workflow

```
[Birth Data] -----> [Calculate Natal Moon] -----> [Create Base Profile]
                                                          |
[--as-of time] --> [Calculate Transit Moon] -> [Compute Aspects] -> [Apply Transit Modifiers]
                                                                              |
                                                          +-------------------+
                                                          |
                                               [Spotify available?]
                                               /                  \
                                            Yes                    No
                                             |                      |
                                    [Fetch Candidates]    [Offline Preview Tracks]
                                    [Score & Rank]                  |
                                    [Diversity + Flow]              |
                                    [Publish Playlist]              |
                                             \                     /
                                              +----> [Output] <---+
                                               plain text / --json / --explain
```

---

### 6. Output Formats

The CLI (`moontuner/cli.py`) supports three output modes:

| Flag | Output |
|---|---|
| *(default)* | Human-readable plain text |
| `--explain` | Plain text + astrological explanation block |
| `--json` | Machine-readable JSON (astrology summary + playlist) |

---

### 7. Quality and Testing

- **Astrological accuracy**: Swiss Ephemeris when installed; otherwise
  approximation with ~1-2 degree typical error.
- **Scoring determinism**: given the same candidate tracks and profile, the
  same ranked list is always produced.
- **Unit tests** in `tests/` cover:
  - `moon_longitude` and `moon_degree_within_sign` correctness
  - Aspect detection and intensity for fixed longitudes
  - Track scoring (good match > poor match)
  - Diversity constraints (artist repeat limits)
  - Flow ordering (all inputs preserved, length unchanged)

---

### 8. Ethical Considerations

- **Privacy**: birth data is only used in-memory for calculation; it is never
  logged or persisted by the library itself.
- **Transparency**: `--explain` prints the full reasoning chain so users
  understand exactly how their data influenced the playlist.
- **Flexibility**: `--moon-sign` and `--phase` overrides let users correct or
  experiment without re-entering birth data.
- **Accuracy disclosure**: the CLI always shows whether calculations used
  Swiss Ephemeris or the built-in approximation.
