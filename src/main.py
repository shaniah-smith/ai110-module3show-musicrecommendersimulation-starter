"""
Command line runner for the Music Recommender Simulation.

Run from the project folder with:  python -m src.main
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

PROFILES = {
    "Happy Pop (default)": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Edge cases designed to "trick" the scoring logic
    "Edge: High-Energy but Sad": {"genre": "indie", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    "Edge: Genre Not in Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
}

# Phase 4 experiment: double energy, halve genre
EXPERIMENT_WEIGHTS = {**DEFAULT_WEIGHTS, "energy": DEFAULT_WEIGHTS["energy"] * 2, "genre": DEFAULT_WEIGHTS["genre"] / 2}


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5, weights: dict = None) -> None:
    """Print a profile's top k songs with scores and reasons."""
    print("=" * 72)
    print(f"Profile: {name}")
    print(f"Prefs:   genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']}, "
          f"likes_acoustic={prefs['likes_acoustic']}")
    print("-" * 72)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}, {song['mood']}]")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    """Load the catalog, then show recommendations for every test profile and the weight experiment."""
    songs = load_songs("data/songs.csv")
    print()

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    print("#" * 72)
    print("EXPERIMENT: energy weight doubled (2.0), genre weight halved (0.5)")
    print("#" * 72)
    print_recommendations("Happy Pop (experiment weights)", PROFILES["Happy Pop (default)"], songs,
                          weights=EXPERIMENT_WEIGHTS)


if __name__ == "__main__":
    main()
