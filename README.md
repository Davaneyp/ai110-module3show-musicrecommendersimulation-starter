# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

This content-based recommender compares each song's attributes with the user's stated preferences. A `UserProfile` stores a favorite genre, a favorite mood, a target energy level (0–1), whether the user likes acoustic music, and a target valence (how positive the music sounds). Each song is scored on five features: +2.0 for a genre match, +1.0 for a mood match, up to +1.5 for energy closeness (`1.5 × (1 - |song.energy - target_energy|)`), up to +1.0 for acoustic fit, and up to +0.5 for valence closeness, for a maximum of 6.0. Energy is scored by closeness rather than raw value, so a user who wants calm music isn't handed the most intense track. Genre is weighted above mood because it reflects lasting taste, while mood changes with the moment. Tempo and danceability are left out because they rise and fall with energy. To recommend songs, the system scores every song in the catalog, sorts them from highest to lowest, and returns the top `k` with a short explanation of each score. Keeping scoring and ranking separate means the weights can be tuned without changing the list logic.

**Algorithm Recipe**

1. Load every song from `data/songs.csv`.
2. For each song, start at 0 points and add:
   - +2.0 if the genre matches the user's favorite genre
   - +1.0 if the mood matches the user's favorite mood
   - up to +1.5 for how close the energy is to the target
   - up to +1.0 for how well the acousticness fits the user's acoustic preference
   - up to +0.5 for how close the valence is to the target
3. Sort all songs from highest to lowest score.
4. Return the top `k` songs, each with the reasons behind its score.

**Expected Biases**

- **Genre dominates.** A genre match is worth twice a mood match, so a song in the right genre but the wrong mood can outrank a song with the right mood. For example, a "happy pop" user may get an intense workout pop song ahead of a happy indie pop song.
- **Exact labels only.** "pop" and "indie pop" count as different genres, and "chill," "relaxed," and "focused" count as different moods, even though they are close in meaning.
- **Small, uneven catalog.** Most genres have only one song, so users with less common tastes get one real match and then songs from other genres.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



