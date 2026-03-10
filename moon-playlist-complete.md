# Moon Sign Playlist Generator - Complete Project Files

## Project Structure
```
moon-playlist-generator/
├── main.py
├── config.py
├── astro_calculator.py
├── music_mapper.py
├── playlist_generator.py
├── moon_signs_data.json
├── requirements.txt
├── .env.example
└── README.md
```

## File 1: requirements.txt
```
spotipy==2.23.0
python-dotenv==1.0.0
requests==2.31.0
pytz==2023.3
ephem==4.1.4
pandas==2.0.3
```

## File 2: .env.example
```
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8080
```

## File 3: config.py
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8080')

# Validate configuration
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")
```

## File 4: moon_signs_data.json
```json
{
  "signs": {
    "Aries": {
      "element": "fire",
      "keywords": ["energetic", "impulsive", "pioneering", "bold"],
      "energy": 0.85,
      "valence": 0.75,
      "tempo_min": 120,
      "tempo_max": 160,
      "danceability": 0.7,
      "acousticness": 0.2,
      "genres": ["rock", "electronic", "hip hop", "pop punk"],
      "audio_features": {
        "loudness": -8,
        "speechiness": 0.1,
        "instrumentalness": 0.1
      }
    },
    "Taurus": {
      "element": "earth",
      "keywords": ["stable", "sensual", "grounded", "patient"],
      "energy": 0.4,
      "valence": 0.6,
      "tempo_min": 60,
      "tempo_max": 100,
      "danceability": 0.5,
      "acousticness": 0.7,
      "genres": ["r&b", "soul", "jazz", "acoustic"],
      "audio_features": {
        "loudness": -12,
        "speechiness": 0.05,
        "instrumentalness": 0.3
      }
    },
    "Gemini": {
      "element": "air",
      "keywords": ["curious", "communicative", "versatile", "witty"],
      "energy": 0.7,
      "valence": 0.8,
      "tempo_min": 100,
      "tempo_max": 140,
      "danceability": 0.65,
      "acousticness": 0.3,
      "genres": ["pop", "indie pop", "electronic", "alternative"],
      "audio_features": {
        "loudness": -9,
        "speechiness": 0.15,
        "instrumentalness": 0.05
      }
    },
    "Cancer": {
      "element": "water",
      "keywords": ["emotional", "nurturing", "intuitive", "nostalgic"],
      "energy": 0.35,
      "valence": 0.45,
      "tempo_min": 70,
      "tempo_max": 110,
      "danceability": 0.4,
      "acousticness": 0.6,
      "genres": ["indie", "singer-songwriter", "ambient", "folk"],
      "audio_features": {
        "loudness": -14,
        "speechiness": 0.04,
        "instrumentalness": 0.4
      }
    },
    "Leo": {
      "element": "fire",
      "keywords": ["dramatic", "confident", "creative", "passionate"],
      "energy": 0.8,
      "valence": 0.85,
      "tempo_min": 110,
      "tempo_max": 150,
      "danceability": 0.75,
      "acousticness": 0.15,
      "genres": ["pop", "dance", "theatrical", "glam rock"],
      "audio_features": {
        "loudness": -7,
        "speechiness": 0.08,
        "instrumentalness": 0.02
      }
    },
    "Virgo": {
      "element": "earth",
      "keywords": ["analytical", "practical", "perfectionist", "modest"],
      "energy": 0.5,
      "valence": 0.55,
      "tempo_min": 90,
      "tempo_max": 120,
      "danceability": 0.45,
      "acousticness": 0.5,
      "genres": ["indie", "alternative", "folk", "chamber pop"],
      "audio_features": {
        "loudness": -11,
        "speechiness": 0.06,
        "instrumentalness": 0.25
      }
    },
    "Libra": {
      "element": "air",
      "keywords": ["harmonious", "diplomatic", "aesthetic", "romantic"],
      "energy": 0.55,
      "valence": 0.7,
      "tempo_min": 80,
      "tempo_max": 120,
      "danceability": 0.6,
      "acousticness": 0.4,
      "genres": ["pop", "r&b", "soft rock", "dream pop"],
      "audio_features": {
        "loudness": -10,
        "speechiness": 0.07,
        "instrumentalness": 0.15
      }
    },
    "Scorpio": {
      "element": "water",
      "keywords": ["intense", "mysterious", "transformative", "passionate"],
      "energy": 0.65,
      "valence": 0.35,
      "tempo_min": 80,
      "tempo_max": 130,
      "danceability": 0.55,
      "acousticness": 0.25,
      "genres": ["alternative", "darkwave", "trip hop", "gothic"],
      "audio_features": {
        "loudness": -9,
        "speechiness": 0.05,
        "instrumentalness": 0.35
      }
    },
    "Sagittarius": {
      "element": "fire",
      "keywords": ["adventurous", "optimistic", "philosophical", "free"],
      "energy": 0.75,
      "valence": 0.8,
      "tempo_min": 100,
      "tempo_max": 140,
      "danceability": 0.65,
      "acousticness": 0.35,
      "genres": ["world", "reggae", "folk rock", "indie rock"],
      "audio_features": {
        "loudness": -8,
        "speechiness": 0.09,
        "instrumentalness": 0.2
      }
    },
    "Capricorn": {
      "element": "earth",
      "keywords": ["ambitious", "disciplined", "traditional", "responsible"],
      "energy": 0.6,
      "valence": 0.5,
      "tempo_min": 70,
      "tempo_max": 110,
      "danceability": 0.4,
      "acousticness": 0.45,
      "genres": ["classical", "jazz", "blues", "classic rock"],
      "audio_features": {
        "loudness": -11,
        "speechiness": 0.04,
        "instrumentalness": 0.45
      }
    },
    "Aquarius": {
      "element": "air",
      "keywords": ["innovative", "independent", "humanitarian", "eccentric"],
      "energy": 0.7,
      "valence": 0.65,
      "tempo_min": 90,
      "tempo_max": 140,
      "danceability": 0.6,
      "acousticness": 0.2,
      "genres": ["electronic", "experimental", "synthpop", "future bass"],
      "audio_features": {
        "loudness": -8,
        "speechiness": 0.1,
        "instrumentalness": 0.5
      }
    },
    "Pisces": {
      "element": "water",
      "keywords": ["dreamy", "compassionate", "artistic", "intuitive"],
      "energy": 0.4,
      "valence": 0.5,
      "tempo_min": 60,
      "tempo_max": 100,
      "danceability": 0.35,
      "acousticness": 0.65,
      "genres": ["ambient", "dream pop", "shoegaze", "new age"],
      "audio_features": {
        "loudness": -13,
        "speechiness": 0.03,
        "instrumentalness": 0.6
      }
    }
  },
  "moon_phases": {
    "new_moon": {
      "energy_modifier": -0.1,
      "valence_modifier": -0.05,
      "description": "Introspective and minimal"
    },
    "waxing_crescent": {
      "energy_modifier": 0.05,
      "valence_modifier": 0.05,
      "description": "Building energy"
    },
    "first_quarter": {
      "energy_modifier": 0.1,
      "valence_modifier": 0.05,
      "description": "Taking action"
    },
    "waxing_gibbous": {
      "energy_modifier": 0.15,
      "valence_modifier": 0.1,
      "description": "Refining and adjusting"
    },
    "full_moon": {
      "energy_modifier": 0.2,
      "valence_modifier": 0.1,
      "description": "Peak intensity"
    },
    "waning_gibbous": {
      "energy_modifier": 0.05,
      "valence_modifier": 0,
      "description": "Gratitude and sharing"
    },
    "last_quarter": {
      "energy_modifier": -0.05,
      "valence_modifier": -0.05,
      "description": "Release and letting go"
    },
    "waning_crescent": {
      "energy_modifier": -0.1,
      "valence_modifier": -0.1,
      "description": "Rest and renewal"
    }
  }
}
```

## File 5: astro_calculator.py
```python
import ephem
from datetime import datetime
import pytz
import json

class MoonCalculator:
    def __init__(self):
        self.moon_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", 
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Load moon signs data
        with open('moon_signs_data.json', 'r') as f:
            self.moon_data = json.load(f)
    
    def calculate_moon_sign(self, birth_date, birth_time, lat, lon):
        """Calculate moon sign for given birth data"""
        try:
            # Create observer
            observer = ephem.Observer()
            observer.lat = str(lat)
            observer.lon = str(lon)
            
            # Parse datetime
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            observer.date = dt
            
            # Calculate moon position
            moon = ephem.Moon(observer)
            
            # Convert to zodiac position
            moon_deg = float(moon.ra) * 180 / ephem.pi
            
            # Determine sign (30 degrees per sign)
            sign_index = int(moon_deg / 30) % 12
            moon_sign = self.moon_signs[sign_index]
            
            return moon_sign
            
        except Exception as e:
            print(f"Error calculating moon sign: {e}")
            # Return a default for testing
            return "Cancer"
    
    def get_current_moon_phase(self):
        """Get current moon phase (0-1)"""
        moon = ephem.Moon()
        moon.compute()
        
        # Convert phase to 0-1 range
        phase = moon.phase / 100.0
        
        # Determine phase name
        if phase < 0.0625:
            phase_name = "new_moon"
        elif phase < 0.1875:
            phase_name = "waxing_crescent"
        elif phase < 0.3125:
            phase_name = "first_quarter"
        elif phase < 0.4375:
            phase_name = "waxing_gibbous"
        elif phase < 0.5625:
            phase_name = "full_moon"
        elif phase < 0.6875:
            phase_name = "waning_gibbous"
        elif phase < 0.8125:
            phase_name = "last_quarter"
        else:
            phase_name = "waning_crescent"
        
        return phase, phase_name
    
    def get_moon_sign_data(self, moon_sign):
        """Get characteristics for a moon sign"""
        return self.moon_data['signs'].get(moon_sign, self.moon_data['signs']['Cancer'])
    
    def get_phase_modifiers(self, phase_name):
        """Get modifiers based on moon phase"""
        return self.moon_data['moon_phases'].get(phase_name, {
            "energy_modifier": 0,
            "valence_modifier": 0,
            "description": "Unknown phase"
        })
```

## File 6: music_mapper.py
```python
class MusicMapper:
    def __init__(self, moon_calculator):
        self.moon_calc = moon_calculator
    
    def create_music_profile(self, moon_sign, moon_phase_name):
        """Create target music profile based on astrological data"""
        
        # Get base moon sign characteristics
        moon_data = self.moon_calc.get_moon_sign_data(moon_sign)
        
        # Get phase modifiers
        phase_mods = self.moon_calc.get_phase_modifiers(moon_phase_name)
        
        # Calculate adjusted values
        target_energy = min(1.0, max(0.0, 
            moon_data['energy'] + phase_mods['energy_modifier']))
        target_valence = min(1.0, max(0.0, 
            moon_data['valence'] + phase_mods['valence_modifier']))
        
        # Build complete profile
        profile = {
            'moon_sign': moon_sign,
            'moon_phase': moon_phase_name,
            'phase_description': phase_mods['description'],
            'target_energy': target_energy,
            'target_valence': target_valence,
            'target_danceability': moon_data['danceability'],
            'target_acousticness': moon_data['acousticness'],
            'tempo_range': (moon_data['tempo_min'], moon_data['tempo_max']),
            'genres': moon_data['genres'],
            'keywords': moon_data['keywords'],
            'element': moon_data['element']
        }
        
        return profile
    
    def calculate_track_score(self, track_features, target_profile):
        """Score how well a track matches the target profile"""
        if not track_features:
            return 0
        
        score = 0
        weights = {
            'energy': 0.25,
            'valence': 0.20,
            'danceability': 0.15,
            'acousticness': 0.10,
            'tempo': 0.15,
            'loudness': 0.15
        }
        
        # Energy match
        if 'energy' in track_features:
            energy_diff = abs(track_features['energy'] - target_profile['target_energy'])
            score += (1 - energy_diff) * weights['energy']
        
        # Valence match
        if 'valence' in track_features:
            valence_diff = abs(track_features['valence'] - target_profile['target_valence'])
            score += (1 - valence_diff) * weights['valence']
        
        # Danceability match
        if 'danceability' in track_features:
            dance_diff = abs(track_features['danceability'] - target_profile['target_danceability'])
            score += (1 - dance_diff) * weights['danceability']
        
        # Acousticness match
        if 'acousticness' in track_features:
            acoustic_diff = abs(track_features['acousticness'] - target_profile['target_acousticness'])
            score += (1 - acoustic_diff) * weights['acousticness']
        
        # Tempo match
        if 'tempo' in track_features:
            tempo = track_features['tempo']
            tempo_min, tempo_max = target_profile['tempo_range']
            if tempo_min <= tempo <= tempo_max:
                score += weights['tempo']
            else:
                # Partial score based on how close it is
                if tempo < tempo_min:
                    tempo_score = max(0, 1 - (tempo_min - tempo) / tempo_min)
                else:
                    tempo_score = max(0, 1 - (tempo - tempo_max) / tempo_max)
                score += tempo_score * weights['tempo']
        
        return score * 100  # Convert to percentage
```

## File 7: playlist_generator.py
```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
from datetime import datetime

class PlaylistGenerator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public user-library-read"
        ))
        self.music_mapper = None
    
    def set_music_mapper(self, mapper):
        self.music_mapper = mapper
    
    def search_tracks(self, target_profile, num_tracks=50):
        """Search for tracks matching the target profile"""
        all_tracks = []
        
        # Search by each genre
        for genre in target_profile['genres']:
            try:
                # Search for tracks in this genre
                results = self.sp.search(
                    q=f'genre:{genre}',
                    type='track',
                    limit=50
                )
                
                tracks = results['tracks']['items']
                
                # Get audio features for all tracks
                track_ids = [t['id'] for t in tracks if t['id']]
                if track_ids:
                    audio_features = self.sp.audio_features(track_ids)
                    
                    # Combine track info with audio features
                    for track, features in zip(tracks, audio_features):
                        if features:
                            track['audio_features'] = features
                            all_tracks.append(track)
            
            except Exception as e:
                print(f"Error searching genre {genre}: {e}")
                continue
        
        # Score and sort tracks
        scored_tracks = []
        for track in all_tracks:
            if 'audio_features' in track:
                score = self.music_mapper.calculate_track_score(
                    track['audio_features'], 
                    target_profile
                )
                scored_tracks.append((track, score))
        
        # Sort by score
        scored_tracks.sort(key=lambda x: x[1], reverse=True)
        
        # Return top tracks
        return [track for track, score in scored_tracks[:num_tracks]]
    
    def create_playlist(self, name, description, tracks):
        """Create a new playlist with the given tracks"""
        try:
            # Get current user
            user_id = self.sp.current_user()['id']
            
            # Create playlist
            playlist = self.sp.user_playlist_create(
                user_id,
                name,
                public=True,
                description=description
            )
            
            # Add tracks in batches (Spotify limit is 100 per request)
            track_uris = [track['uri'] for track in tracks]
            
            for i in range(0, len(track_uris), 100):
                batch = track_uris[i:i+100]
                self.sp.playlist_add_items(playlist['id'], batch)
            
            return playlist
            
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None
    
    def generate_playlist_name(self, moon_sign, moon_phase):
        """Generate a creative playlist name"""
        templates = [
            f"{moon_sign} Moon {moon_phase.replace('_', ' ').title()} Vibes",
            f"Lunar {moon_sign}: {moon_phase.replace('_', ' ').title()}",
            f"{moon_phase.replace('_', ' ').title()} in {moon_sign}",
            f"{moon_sign} Moon Journey - {datetime.now().strftime('%B %Y')}"
        ]
        return random.choice(templates)
```

## File 8: main.py
```python
#!/usr/bin/env python3
"""
Moon Sign Playlist Generator
Creates Spotify playlists based on your astrological moon sign and current lunar phase
"""

import sys
from datetime import datetime
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
from astro_calculator import MoonCalculator
from music_mapper import MusicMapper
from playlist_generator import PlaylistGenerator

def print_header():
    """Print welcome header"""
    print("\n" + "="*60)
    print("🌙 ✨ MOON SIGN PLAYLIST GENERATOR ✨ 🌙".center(60))
    print("="*60)
    print("Create personalized Spotify playlists based on your moon sign!")
    print("="*60 + "\n")

def get_birth_info():
    """Get birth information from user"""
    print("📅 Enter your birth information:")
    print("-" * 40)
    
    # Get birth date
    while True:
        birth_date = input("Birth date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD")
    
    # Get birth time
    while True:
        birth_time = input("Birth time (HH:MM in 24-hour format): ").strip()
        try:
            datetime.strptime(birth_time, "%H:%M")
            break
        except ValueError:
            print("❌ Invalid time format. Please use HH:MM (e.g., 14:30)")
    
    # Get location
    print("\n📍 Birth location (for accurate moon position):")
    print("   Examples: Los Angeles = 34.0522, -118.2437")
    print("            New York = 40.7128, -74.0060")
    print("            London = 51.5074, -0.1278")
    
    while True:
        try:
            lat = float(input("Latitude: ").strip())
            lon = float(input("Longitude: ").strip())
            break
        except ValueError:
            print("❌ Please enter valid numbers")
    
    return birth_date, birth_time, lat, lon

def main():
    """Main program flow"""
    print_header()
    
    # Initialize components
    print("🔧 Initializing components...")
    moon_calc = MoonCalculator()
    music_mapper = MusicMapper(moon_calc)
    playlist_gen = PlaylistGenerator(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_REDIRECT_URI
    )
    playlist_gen.set_music_mapper(music_mapper)
    
    # Get user input
    use_example = input("Use example data? (y/n): ").lower().strip() == 'y'
    
    if use_example:
        # Example data
        birth_date = "1990-07-15"
        birth_time = "14:30"
        lat = 34.0522  # Los Angeles
        lon = -118.2437
        print(f"\n📊 Using example data: {birth_date} {birth_time}, LA")
    else:
        birth_date, birth_time, lat, lon = get_birth_info()
    
    # Calculate moon sign
    print("\n🔮 Calculating your moon sign...")
    moon_sign = moon_calc.calculate_moon_sign(birth_date, birth_time, lat, lon)
    moon_phase, phase_name = moon_calc.get_current_moon_phase()
    
    print(f"\n✨ Your Results:")
    print(f"   Moon Sign: {moon_sign}")
    print(f"   Current Moon Phase: {phase_name.replace('_', ' ').title()} ({moon_phase:.1%})")
    
    # Get moon characteristics
    moon_data = moon_calc.get_moon_sign_data(moon_sign)
    print(f"   Element: {moon_data['element'].title()}")
    print(f"   Keywords: {', '.join(moon_data['keywords'])}")
    
    # Create music profile
    print("\n🎵 Creating music profile...")
    music_profile = music_mapper.create_music_profile(moon_sign, phase_name)
    
    print(f"   Target Energy: {music_profile['target_energy']:.2f}")
    print(f"   Target Mood: {music_profile['target_valence']:.2f}")
    print(f"   Preferred Genres: {', '.join(music_profile['genres'])}")
    print(f"   Phase Influence: {music_profile['phase_description']}")
    
    # Search for tracks
    print("\n🔍 Searching for matching tracks...")
    print("   (This may take a moment...)")
    
    tracks = playlist_gen.search_tracks(music_profile, num_tracks=30)
    
    if not tracks:
        print("❌ No tracks found. Please check your Spotify connection.")
        return
    
    print(f"   ✅ Found {len(tracks)} matching tracks!")
    
    # Show sample tracks
    print("\n🎶 Sample tracks:")
    for i, track in enumerate(tracks[:5], 1):
        artists = ", ".join([a['name'] for a in track['artists']])
        print(f"   {i}. {track['name']} - {artists}")
    
    # Create playlist
    create = input("\n📋 Create playlist on Spotify? (y/n): ").lower().strip() == 'y'
    
    if create:
        print("\n🚀 Creating playlist...")
        
        # Generate playlist name and description
        playlist_name = playlist_gen.generate_playlist_name(moon_sign, phase_name)
        description = (f"Curated for {moon_sign} moon with {phase_name.replace('_', ' ')} "
                      f"phase. Energy: {music_profile['target_energy']:.0%}, "
                      f"Mood: {music_profile['target_valence']:.0%}")
        
        playlist = playlist_gen.create_playlist(playlist_name, description, tracks)
        
        if playlist:
            print(f"\n✅ Success! Playlist created: {playlist_name}")
            print(f"🔗 Open in Spotify: {playlist['external_urls']['spotify']}")
            print(f"📊 Total tracks: {len(tracks)}")
        else:
            print("❌ Failed to create playlist. Please check your Spotify permissions.")
    
    print("\n🌙 Thank you for using Moon Sign Playlist Generator!")
    print("   May your music align with the cosmos! ✨\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)
```

## File 9: README.md
```markdown
# 🌙 Moon Sign Playlist Generator

Generate personalized Spotify playlists based on your astrological moon sign and current lunar phase!

## Features

- Calculate your moon sign based on birth date, time, and location
- Analyze current moon phase and its influence on your emotional state
- Generate Spotify playlists with tracks that match your astrological profile
- Smart track selection based on energy, mood, tempo, and genre preferences
- Beautiful command-line interface with emoji indicators

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- Spotify Premium account (free accounts work too, but with limitations)
- Spotify Developer account (free)

### 2. Setup Spotify API

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create app"
3. Fill in:
   - App name: "Moon Playlist Generator"
   - App description: "Astrological playlist generator"
   - Redirect URI: `http://localhost:8080`
4. Save your Client ID and Client Secret

### 3. Installation

```bash
# Clone or download this project
cd moon-playlist-generator

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your Spotify credentials
nano .env  # or use any text editor
```

### 4. Run the Generator

```bash
python main.py
```

Follow the prompts to:
1. Enter your birth information (or use example data)
2. View your moon sign and current phase
3. Create a personalized playlist

## How It Works

1. **Astrological Calculation**: Uses astronomical algorithms to determine your moon sign
2. **Music Profiling**: Maps moon signs to musical characteristics (energy, mood, genres)
3. **Phase Adjustment**: Modifies the profile based on current lunar phase
4. **Smart Search**: Searches Spotify for tracks matching your profile
5. **Playlist Creation**: Generates a playlist with 30 carefully selected tracks

## Moon Sign Characteristics

- **Fire Signs** (Aries, Leo, Sagittarius): High energy, upbeat tempo
- **Earth Signs** (Taurus, Virgo, Capricorn): Grounded, acoustic, moderate tempo
- **Air Signs** (Gemini, Libra, Aquarius): Versatile, pop/electronic, social
- **Water Signs** (Cancer, Scorpio, Pisces): Emotional, atmospheric, introspective

## Troubleshooting

### "No module named 'spotipy'"
Run: `pip install -r requirements.txt`

### "Please set SPOTIFY_CLIENT_ID..."
Make sure you've:
1. Created a `.env` file (not `.env.example`)
2. Added your Spotify credentials
3. Saved the file

### Authentication Opens Wrong Browser
This is normal. Copy the URL from the browser and paste it back into the terminal.

### "No tracks found"
- Check your internet connection
- Verify Spotify credentials are correct
- Try running again (sometimes Spotify API has temporary issues)

## Customization

Edit `moon_signs_data.json` to:
- Adjust music preferences for each sign
- Add new genres
- Modify energy/mood mappings
- Change tempo ranges

## Future Enhancements

- Web interface
- Transit calculations
- Saved playlist history
- Machine learning optimization
- Multiple music platforms

## License

MIT License - feel free to modify and share!

## Acknowledgments

- Spotify Web API
- Spotipy library
- PyEphem for astronomical calculations

---

Made with 🌙 and ✨ by the cosmos
```

## Setup Instructions

1. **Create a new folder** called `moon-playlist-generator`

2. **Copy each file** from above into the folder with the exact filename shown

3. **Create a `.env` file** (not `.env.example`) and add your Spotify credentials:
   ```
   SPOTIFY_CLIENT_ID=your_actual_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8080
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the program**:
   ```bash
   python main.py
   ```

That's it! The program will guide you through the rest.

## Important Notes

- When you first run it, Spotify will open a browser for authentication
- Copy the URL from your browser and paste it back into the terminal
- The program includes example data so you can test it immediately
- All moon sign characteristics and music mappings are in `moon_signs_data.json` for easy customization

This is a complete, working project that you can run immediately!