# 🌙 MoonTuner Playlist Generator

MoonTuner turns your natal moon sign and current lunar transits into a playlist.
When Spotify credentials are available it fetches real tracks, scores them against
an astrological mood profile using audio features (energy, valence, tempo,
danceability), enforces artist diversity, and orders them in a flowing energy arc.
Without credentials it falls back to a deterministic offline preview — so it always
works.

---

## Installation

**Python 3.10+ required.**

```bash
# Clone and enter the repo
git clone https://github.com/michaelanticoli/moontuner-playlist.git
cd moontuner-playlist

# Install core (stdlib only — no Spotify, no Swiss Ephemeris)
pip install -e .

# Install with Spotify support
pip install -e ".[spotify]"

# Install with Swiss Ephemeris (higher-precision moon calculations)
pip install -e ".[ephemeris]"

# Install with both
pip install -e ".[spotify,ephemeris]"
```

After installation the `moontuner` console script is available:

```bash
moontuner --help
```

You can also run without installing:

```bash
python main.py --help
```

---

## Spotify Setup

1. Go to <https://developer.spotify.com/dashboard> and create an app.
2. Add `http://localhost:8080/callback` to your app's Redirect URIs.
3. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```ini
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

4. Run with `--publish-spotify`. Your browser will open for the OAuth flow on
   the first run; after that a token cache handles re-authentication.

---

## Usage

### Basic (offline preview)

```bash
moontuner --birth-date 1990-07-15 --birth-time 14:30 --count 10
```

### Override the reading directly

```bash
moontuner --moon-sign Aries --phase full_moon --count 10
```

### Astrological explanation (`--explain`)

```bash
moontuner --birth-date 1990-07-15 --birth-time 14:30 --count 5 --explain
```

Output:
```
🌙 MoonTuner Playlist Generator
Natal moon: Aries 24.7° (approximation)
Moon phase: last quarter
Transit moon: Libra 25.9°
Energy target: 0.76
Mood target: 0.62
...

── Astrological Explanation ──────────────────────────
  Natal moon in Aries at 24.7° (longitude 24.7°)
  Aries is a fire sign: energetic, impulsive, pioneering, bold
  Phase 'last quarter': Release and letting go
  Active transit aspects to natal moon:
    • Opposition (orb 1.3°, intensity 84%): Current moon opposite natal moon: inner tension and reflection
  Final targets — energy: 0.76, valence: 0.62
──────────────────────────────────────────────────────
```

### JSON output (`--json`)

```bash
moontuner --birth-date 1990-07-15 --birth-time 14:30 --count 3 --json
```

```json
{
  "astrology": {
    "natal_moon_sign": "Aries",
    "natal_moon_degree": 24.66,
    "natal_moon_longitude": 24.66,
    "moon_phase": "last_quarter",
    "source": "approximation",
    "transit_moon_sign": "Libra",
    "transit_moon_longitude": 205.93,
    "aspects": [
      {
        "name": "opposition",
        "orb": 1.27,
        "intensity": 0.841,
        "description": "Current moon opposite natal moon: inner tension and reflection"
      }
    ]
  },
  "profile": { "target_energy": 0.758, "target_valence": 0.616, "genres": ["rock", "..."] },
  "playlist": { "name": "Aries Moon • Last Quarter", "tracks": [...] }
}
```

### Custom transit time (`--as-of`)

```bash
# See what the playlist would have been on the summer solstice 2024
moontuner --birth-date 1990-07-15 --birth-time 14:30 --as-of "2024-06-21 18:00" --explain
```

### Publish to Spotify

```bash
moontuner --birth-date 1990-07-15 --birth-time 14:30 --count 20 --publish-spotify
```

---

## Astrological Accuracy

| Mode | When active | Typical accuracy |
|---|---|---|
| Swiss Ephemeris | `pyswisseph` installed | < 0.01° |
| Built-in approximation | always | ~1-2° |

The source used is always printed in the output (`approximation` or `swisseph`).

---

## How It Works

1. **Natal moon** is calculated from your birth date/time.
2. **Transit moon** is calculated for the current moment (or `--as-of`).
3. **Aspects** between the two longitudes are detected (conjunction, sextile,
   square, trine, opposition) with orb and intensity.
4. A **mood profile** is built from the natal moon sign + phase, then adjusted
   by transit modifiers scaled by aspect intensity.
5. **Tracks** are selected:
   - *With Spotify*: from your top tracks, saved library, and genre
     recommendations; scored against `target_energy`, `target_valence`, tempo,
     and danceability; diversity-filtered; ordered in an energy arc.
   - *Without Spotify*: a themed deterministic preview list.

See [`moon-sign-playlist-algorithm.md`](moon-sign-playlist-algorithm.md) for
full algorithmic detail.

---

## Tests

```bash
python -m unittest discover -s tests -v
```

CI runs the same suite on Python 3.10 and 3.12 on every push, plus `ruff`
for formatting and lint.

---

## Contributing

Formatting and lint are enforced by `ruff`:

```bash
pip install "ruff>=0.4"
ruff check moontuner tests
ruff format moontuner tests
```
