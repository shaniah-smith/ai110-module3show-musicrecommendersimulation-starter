"""
Command line runner for the Music Recommender Simulation.

Run from the project folder with:
    python -m src.main                       # default Mood-First mode
    python -m src.main --mode genre_first    # switch scoring mode (Challenge 2)
    python -m src.main --mode energy_focused
"""

import argparse

from src.recommender import (
    DEFAULT_WEIGHTS,
    SCORING_MODES,
    load_songs,
    recommend_diverse,
    recommend_songs,
    recommend_with_mode,
)

try:  # Challenge 4: formatted tables
    from tabulate import tabulate
except ImportError:  # still runs without tabulate, just plainer
    tabulate = None

PROFILES = {
    "Happy Pop (default)": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Edge cases designed to "trick" the scoring logic
    "Edge: High-Energy but Sad": {"genre": "indie", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    "Edge: Genre Not in Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
}

# Challenge 1: a profile that uses the new advanced features
ADVANCED_PROFILE = {
    "genre": "jazz", "mood": "relaxed", "energy": 0.4, "likes_acoustic": True,
    "preferred_decade": "2010s", "mood_tags": ["cozy", "late-night"],
    "popularity_pref": "underground", "focus_mode": True,
}

# Phase 4 experiment: double energy, halve genre
EXPERIMENT_WEIGHTS = {**DEFAULT_WEIGHTS, "energy": DEFAULT_WEIGHTS["energy"] * 2, "genre": DEFAULT_WEIGHTS["genre"] / 2}


def describe(prefs: dict) -> str:
    """Turn a prefs dict into one readable line."""
    return ", ".join(f"{k}={v}" for k, v in prefs.items())


def print_table(title: str, prefs: dict, results: list) -> None:
    """Print ranked results as a table with each reason on its own line."""
    print("=" * 78)
    print(f"Profile: {title}")
    print(f"Prefs:   {describe(prefs)}")
    rows = [
        [rank, f"{song['title']}\n{song['artist']}", f"{song['genre']}\n{song['mood']}",
         f"{score:.2f}", explanation.replace("; ", "\n")]
        for rank, (song, score, explanation) in enumerate(results, start=1)
    ]
    headers = ["#", "Song / Artist", "Genre / Mood", "Score", "Why it was picked"]
    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        for row in rows:
            print(f"{row[0]}. {row[1].replace(chr(10), ' by ')}  [{row[2].replace(chr(10), ', ')}]  "
                  f"Score: {row[3]}\n   Because: {row[4].replace(chr(10), '; ')}")
    print()


def main() -> None:
    """Load the catalog, then show recommendations for every profile, experiment, and challenge."""
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=list(SCORING_MODES), default="mood_first",
                        help="scoring strategy to rank the main profiles with")
    args = parser.parse_args()
    mode = SCORING_MODES[args.mode]

    songs = load_songs("data/songs.csv")
    print(f"Scoring mode: {mode.name} ({mode.description})\n")

    for name, prefs in PROFILES.items():
        print_table(name, prefs, recommend_with_mode(prefs, songs, args.mode))

    print("#" * 78)
    print("EXPERIMENT: energy weight doubled (2.0), genre weight halved (0.5)")
    print("#" * 78)
    print_table("Happy Pop (experiment weights)", PROFILES["Happy Pop (default)"],
                recommend_songs(PROFILES["Happy Pop (default)"], songs, weights=EXPERIMENT_WEIGHTS))

    print("#" * 78)
    print("CHALLENGE 1: advanced features (decade, mood tags, popularity, focus mode)")
    print("#" * 78)
    print_table("Late-Night Underground Jazz", ADVANCED_PROFILE, recommend_songs(ADVANCED_PROFILE, songs))

    print("#" * 78)
    print("CHALLENGE 2: same profile, three scoring modes")
    print("#" * 78)
    for key, strategy in SCORING_MODES.items():
        print_table(f"Edge: High-Energy but Sad / {strategy.name}", PROFILES["Edge: High-Energy but Sad"],
                    recommend_with_mode(PROFILES["Edge: High-Energy but Sad"], songs, key))

    print("#" * 78)
    print("CHALLENGE 3: diversity penalty (-1.0 repeat artist, -0.5 repeat genre)")
    print("#" * 78)
    print_table("Chill Lofi (diverse)", PROFILES["Chill Lofi"], recommend_diverse(PROFILES["Chill Lofi"], songs))


if __name__ == "__main__":
    main()
