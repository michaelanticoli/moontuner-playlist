# 🌙 MoonTuner Playlist Generator

MoonTuner is now a small, working Python CLI that turns a user's moon sign and lunar phase into a playlist blueprint. It works offline with the Python standard library and can optionally publish a playlist to Spotify when `spotipy` credentials are available.

## What was finished

The previous Copilot task was cancelled before the repository moved beyond planning docs. This branch completes that work by adding:

- a real `moontuner/` Python package
- a CLI entry point in `main.py`
- approximate moon sign / phase calculation with optional Swiss Ephemeris support
- moon-sign mood mapping
- playlist generation with deterministic preview tracks
- focused regression tests

## Usage

```bash
python main.py --birth-date 1990-07-15 --birth-time 14:30 --count 5
```

You can also override the reading directly:

```bash
python main.py --moon-sign Aries --phase full_moon --count 5
```

## Optional Spotify publishing

Create a `.env` file from `.env.example` and provide Spotify credentials:

```bash
cp .env.example .env
```

Then run:

```bash
python main.py --moon-sign Aries --phase full_moon --publish-spotify
```

If `spotipy` is unavailable or credentials are missing, MoonTuner still produces a local playlist preview instead of failing.

## Tests

```bash
python -m unittest discover -s tests
```
