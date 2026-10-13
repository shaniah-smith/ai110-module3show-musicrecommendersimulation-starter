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
    # Optional Challenge 1: only used when the user sets the matching preference
    "decade": 0.5,       # song is from the user's preferred decade
    "tag": 0.25,         # per shared mood tag (up to 2 tags)
    "popularity": 0.5,   # max points for matching "popular" vs "underground"
    "focus": 0.5,        # max points for instrumental, low-talking songs in focus mode
}

NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness",
                  "popularity", "instrumentalness", "speechiness"}


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
                if field in row:
                    row[field] = float(row[field])
            if "mood_tags" in row:
                row["mood_tags"] = [t.strip() for t in row["mood_tags"].split(";") if t.strip()]
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
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

    # ---- Optional Challenge 1: advanced features (skipped if the user didn't ask) ----
    if user_prefs.get("preferred_decade") and song.get("release_decade") == user_prefs["preferred_decade"]:
        score += w["decade"]
        reasons.append(f"from the {song['release_decade']} (+{w['decade']:.2f})")

    if user_prefs.get("mood_tags") and song.get("mood_tags"):
        shared = [t for t in user_prefs["mood_tags"] if t in song["mood_tags"]][:2]
        if shared:
            points = w["tag"] * len(shared)
            score += points
            reasons.append(f"mood tags {', '.join(shared)} (+{points:.2f})")

    if user_prefs.get("popularity_pref") in ("popular", "underground") and "popularity" in song:
        pop = song["popularity"] / 100
        fit = pop if user_prefs["popularity_pref"] == "popular" else 1 - pop
        points = w["popularity"] * fit
        score += points
        reasons.append(f"{user_prefs['popularity_pref']} fit, popularity {song['popularity']:.0f} (+{points:.2f})")

    if user_prefs.get("focus_mode") and "instrumentalness" in song and "speechiness" in song:
        points = w["focus"] * (song["instrumentalness"] + (1 - song["speechiness"])) / 2
        score += points
        reasons.append(f"focus fit (+{points:.2f})")

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


# ---- Optional Challenge 3: diversity penalty ------------------------------ #
DIVERSITY_PENALTY = {"artist": 1.0, "genre": 0.5}


def recommend_diverse(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None,
    penalty: Optional[Dict] = None,
) -> List[Tuple[Dict, float, str]]:
    """Pick the top k one at a time, lowering a song's score if its artist or genre is already picked."""
    p = penalty or DIVERSITY_PENALTY
    remaining = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        remaining.append((song, score, reasons))

    picked: List[Tuple[Dict, float, str]] = []
    while remaining and len(picked) < k:
        best = None
        for song, score, reasons in remaining:
            adjusted, notes = score, []
            if any(s["artist"] == song["artist"] for s, _, _ in picked):
                adjusted -= p["artist"]
                notes.append(f"artist already in list (-{p['artist']:.1f})")
            if any(s["genre"] == song["genre"] for s, _, _ in picked):
                adjusted -= p["genre"]
                notes.append(f"genre already in list (-{p['genre']:.1f})")
            if best is None or adjusted > best[1]:
                best = (song, round(adjusted, 2), "; ".join(reasons + notes))
        picked.append(best)
        remaining = [r for r in remaining if r[0] is not best[0]]
    return picked


# ---- Optional Challenge 2: scoring modes (Strategy pattern) ---------------- #
class ScoringMode:
    """A scoring strategy: a name, a short description, and the weights it scores with."""

    def __init__(self, name: str, description: str, weights: Dict):
        """Store the strategy's name, description, and weight overrides."""
        self.name = name
        self.description = description
        self.weights = {**DEFAULT_WEIGHTS, **weights}

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        """Score one song using this strategy's weights."""
        return score_song(user_prefs, song, self.weights)


SCORING_MODES = {
    "mood_first": ScoringMode("Mood-First", "Feeling matters most (the default recipe)", {}),
    "genre_first": ScoringMode("Genre-First", "Stick to the user's genre", {"genre": 2.0, "mood": 1.0}),
    "energy_focused": ScoringMode("Energy-Focused", "Match the energy level above all",
                                  {"energy": 2.5, "mood": 1.0, "genre": 0.5}),
}


def recommend_with_mode(
    user_prefs: Dict, songs: List[Dict], mode: str = "mood_first", k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Rank songs with the chosen ScoringMode strategy and return the top k."""
    if mode not in SCORING_MODES:
        raise ValueError(f"Unknown mode {mode!r}. Choose from: {', '.join(SCORING_MODES)}")
    strategy = SCORING_MODES[mode]
    scored = [(song, *strategy.score(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]
