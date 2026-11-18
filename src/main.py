"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs

Run from the project root with:  python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs  # python src/main.py


# Taste profiles. Categorical keys are matched against song genre/mood;
# numeric targets are compared by closeness (0.0-1.0 scale).
PROFILES = {
    # Default profile: an upbeat "happy pop" listener.
    "Happy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_acousticness": 0.20,
    },
    # A late-night "chill lofi" listener.
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_acousticness": 0.80,
    },
}

WIDTH = 64


def format_prefs(prefs: dict) -> str:
    """One-line summary of a user profile."""
    parts = [f"genre={prefs['favorite_genre']}", f"mood={prefs['favorite_mood']}"]
    for key in ("target_energy", "target_valence", "target_acousticness"):
        if key in prefs:
            parts.append(f"{key.replace('target_', '')}={prefs[key]:.2f}")
    return ", ".join(parts)


def print_recommendations(name: str, prefs: dict, recommendations: list) -> None:
    """Print a ranked list of (song, score, explanation) tuples."""
    print("=" * WIDTH)
    print(f"Profile: {name}")
    print(f"  {format_prefs(prefs)}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 6.00   [{song['genre']}, {song['mood']}]")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, prefs, recommendations)


if __name__ == "__main__":
    main()
