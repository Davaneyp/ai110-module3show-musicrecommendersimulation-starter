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
    from src.recommender import load_songs, recommend_songs, MAX_SCORE  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs, MAX_SCORE  # python src/main.py


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
    # A loud, aggressive "deep intense rock" listener.
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.40,
        "target_acousticness": 0.10,
    },
}

# Adversarial / edge-case profiles: designed to see whether the scoring
# logic can be "tricked" or produces surprising rankings.
EDGE_CASE_PROFILES = {
    # Conflicting preferences: a sad mood but very high energy. The only
    # sad song in the catalog is a quiet folk track (energy 0.30).
    "Conflict: Sad but Hyped": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.20,
        "target_acousticness": 0.10,
    },
    # Genre and audio targets disagree: classical fan who wants euphoric,
    # high-energy, electronic-sounding music. Does the +2.0 genre bonus win?
    "Conflict: Euphoric Classical": {
        "favorite_genre": "classical",
        "favorite_mood": "euphoric",
        "target_energy": 0.95,
        "target_valence": 0.90,
        "target_acousticness": 0.05,
    },
    # Genre and mood that do not exist in the catalog: only the numeric
    # features can contribute, so the max reachable score is 3.0.
    "Ghost Genre (k-pop / dreamy)": {
        "favorite_genre": "k-pop",
        "favorite_mood": "dreamy",
        "target_energy": 0.70,
        "target_valence": 0.70,
        "target_acousticness": 0.30,
    },
    # Messy input: odd casing and stray whitespace. Should still match
    # "pop" and "happy" if label matching is normalized.
    "Messy Labels ('  POP ', 'Happy')": {
        "favorite_genre": "  POP ",
        "favorite_mood": "Happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_acousticness": 0.20,
    },
    # Out-of-range targets: nothing clamps inputs to 0-1, so closeness
    # terms can go negative. Does ranking still make sense?
    "Out of Range (energy 1.5, acoustic -0.5)": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 1.5,
        "target_valence": 0.0,
        "target_acousticness": -0.5,
    },
    # Perfectly neutral: no genre/mood, every target at 0.5. Reveals which
    # songs win purely by sitting near the middle of every scale.
    "Dead Center (all 0.5, no labels)": {
        "target_energy": 0.5,
        "target_valence": 0.5,
        "target_acousticness": 0.5,
    },
    # Empty profile: every song scores 0.0, so the "ranking" is just
    # catalog order (stable sort tie-break).
    "Empty Profile": {},
}

WIDTH = 64


def format_prefs(prefs: dict) -> str:
    """One-line summary of a user profile."""
    parts = [
        f"genre={prefs.get('favorite_genre')!r}",
        f"mood={prefs.get('favorite_mood')!r}",
    ]
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
        print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}   [{song['genre']}, {song['mood']}]")
        print("   Reasons:")
        reasons = explanation.split("; ") if explanation else ["(no preferences matched)"]
        for reason in reasons:
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    all_profiles = {**PROFILES, **EDGE_CASE_PROFILES}
    for name, prefs in all_profiles.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, prefs, recommendations)


if __name__ == "__main__":
    main()
