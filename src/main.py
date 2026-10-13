"""
Command line runner for the Music Recommender Simulation.

Run from the project folder with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Load the catalog and print the top 5 recommendations for the default profile."""
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}

    print("\nUser profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False")
    print("Top recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=5), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}, {song['mood']}]")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()
