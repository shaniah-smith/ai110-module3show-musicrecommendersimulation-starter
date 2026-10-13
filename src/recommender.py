"""Content-based music recommender: loads songs, scores them against a taste profile, and ranks them."""

import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

# Algorithm Recipe: mood matters most, then genre, then how close the energy is.
DEFAULT_WEIGHTS = {
    "mood": 2.0,      # exact mood match
    "genre": 1.0,     # exact genre match
    "energy": 1.0,    # max points for a perfect energy match
    "acoustic": 0.5,  # max points for matching the acoustic preference
}

NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile object into the user_prefs dictionary used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        """Store the catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, highest score first."""
        prefs = profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why this song got its score."""
        score, reasons = score_song(profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to numbers."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons: List[str] = []

    if song["mood"].lower() == str(user_prefs.get("mood", "")).lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    if song["genre"].lower() == str(user_prefs.get("genre", "")).lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if "energy" in user_prefs:
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        points = w["energy"] * closeness
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        fit = song["acousticness"] if user_prefs["likes_acoustic"] else 1 - song["acousticness"]
        points = w["acoustic"] * fit
        score += points
        reasons.append(f"acoustic fit (+{points:.2f})")

    return round(score, 2), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort from highest to lowest, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
