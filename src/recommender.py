import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Phase 4 experiment toggle. False = baseline Algorithm Recipe weights.
# True = "Weight Shift": energy doubled (1.5 -> 3.0), genre halved (2.0 -> 1.0).
EXPERIMENT_WEIGHT_SHIFT = False

if EXPERIMENT_WEIGHT_SHIFT:
    GENRE_WEIGHT = 1.0
    ENERGY_WEIGHT = 3.0
else:
    # Scoring weights from the Phase 2 Algorithm Recipe.
    GENRE_WEIGHT = 2.0
    ENERGY_WEIGHT = 1.5
MOOD_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 1.0
VALENCE_WEIGHT = 0.5

# Best possible score: every bonus earned and every closeness term perfect.
# Baseline = 6.0, Weight Shift = 6.5.
MAX_SCORE = GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT + VALENCE_WEIGHT

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting id to int and audio features to float."""
    print(f"Loading songs from {csv_path}...")

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                key = key.strip()
                value = value.strip() if value is not None else value
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max MAX_SCORE) and return (score, list of reasons)."""
    # Algorithm Recipe (Phase 2), max score = MAX_SCORE:
    #   +GENRE_WEIGHT     genre match
    #   +MOOD_WEIGHT      mood match
    #   +ENERGY_WEIGHT    max, energy closeness:   ENERGY_WEIGHT * (1 - |song.energy - target_energy|)
    #   +ACOUSTIC_WEIGHT  max, acoustic fit
    #   +VALENCE_WEIGHT   max, valence closeness:  VALENCE_WEIGHT * (1 - |song.valence - target_valence|)
    # Each closeness term stays in [0, weight] while targets are within 0-1.
    score = 0.0
    reasons: List[str] = []

    # Genre and mood: exact (case-insensitive) label matches.
    fav_genre = user_prefs.get("favorite_genre")
    if fav_genre and song["genre"].strip().lower() == fav_genre.strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.2f})")

    fav_mood = user_prefs.get("favorite_mood")
    if fav_mood and song["mood"].strip().lower() == fav_mood.strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.2f})")

    # Energy: reward closeness to the target, not a high or low value.
    if "target_energy" in user_prefs:
        target = float(user_prefs["target_energy"])
        points = ENERGY_WEIGHT * (1 - abs(song["energy"] - target))
        score += points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target:.2f} (+{points:.2f})"
        )

    # Acoustic fit: a likes_acoustic flag (from UserProfile) rewards high or low
    # acousticness; otherwise a numeric target_acousticness rewards closeness.
    if "likes_acoustic" in user_prefs:
        likes = bool(user_prefs["likes_acoustic"])
        fit = song["acousticness"] if likes else 1 - song["acousticness"]
        points = ACOUSTIC_WEIGHT * fit
        score += points
        pref = "likes" if likes else "avoids"
        reasons.append(
            f"acousticness {song['acousticness']:.2f}, user {pref} acoustic (+{points:.2f})"
        )
    elif "target_acousticness" in user_prefs:
        target = float(user_prefs["target_acousticness"])
        points = ACOUSTIC_WEIGHT * (1 - abs(song["acousticness"] - target))
        score += points
        reasons.append(
            f"acousticness {song['acousticness']:.2f} vs target {target:.2f} (+{points:.2f})"
        )

    # Valence: closeness to how positive the user wants the music to sound.
    if "target_valence" in user_prefs:
        target = float(user_prefs["target_valence"])
        points = VALENCE_WEIGHT * (1 - abs(song["valence"] - target))
        score += points
        reasons.append(
            f"valence {song['valence']:.2f} vs target {target:.2f} (+{points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest to lowest, and return the top k as (song, score, explanation)."""
    # Judge every song with score_song, keeping (song, score, explanation).
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sorted() returns a new list and leaves `songs` untouched.
    # The sort is stable, so tied songs keep their catalog order.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
