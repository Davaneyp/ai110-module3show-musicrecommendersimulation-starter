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
Loading songs from data/songs.csv...
Loaded songs: 20

================================================================
Profile: Happy Pop
  genre=pop, mood=happy, energy=0.80, valence=0.80, acousticness=0.20
================================================================
1. Sunrise City by Neon Echo
   Score: 5.93 / 6.00   [pop, happy]
   Reasons:
     - genre match: pop (+2.00)
     - mood match: happy (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
     - acousticness 0.18 vs target 0.20 (+0.98)
     - valence 0.84 vs target 0.80 (+0.48)

2. Gym Hero by Max Pulse
   Score: 4.64 / 6.00   [pop, intense]
   Reasons:
     - genre match: pop (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
     - acousticness 0.05 vs target 0.20 (+0.85)
     - valence 0.77 vs target 0.80 (+0.48)

3. Rooftop Lights by Indigo Parade
   Score: 3.79 / 6.00   [indie pop, happy]
   Reasons:
     - mood match: happy (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
     - acousticness 0.35 vs target 0.20 (+0.85)
     - valence 0.81 vs target 0.80 (+0.49)

4. Fuego Lento by Sol Marea
   Score: 2.83 / 6.00   [latin, playful]
   Reasons:
     - energy 0.81 vs target 0.80 (+1.48)
     - acousticness 0.30 vs target 0.20 (+0.90)
     - valence 0.90 vs target 0.80 (+0.45)

5. Concrete Crown by Kilo Verse
   Score: 2.80 / 6.00   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 0.80 (+1.47)
     - acousticness 0.12 vs target 0.20 (+0.92)
     - valence 0.62 vs target 0.80 (+0.41)

================================================================
Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.40, valence=0.60, acousticness=0.80
================================================================
1. Library Rain by Paper Lanterns
   Score: 5.87 / 6.00   [lofi, chill]
   Reasons:
     - genre match: lofi (+2.00)
     - mood match: chill (+1.00)
     - energy 0.35 vs target 0.40 (+1.42)
     - acousticness 0.86 vs target 0.80 (+0.94)
     - valence 0.60 vs target 0.60 (+0.50)

2. Midnight Coding by LoRoom
   Score: 5.86 / 6.00   [lofi, chill]
   Reasons:
     - genre match: lofi (+2.00)
     - mood match: chill (+1.00)
     - energy 0.42 vs target 0.40 (+1.47)
     - acousticness 0.71 vs target 0.80 (+0.91)
     - valence 0.56 vs target 0.60 (+0.48)

3. Focus Flow by LoRoom
   Score: 4.98 / 6.00   [lofi, focused]
   Reasons:
     - genre match: lofi (+2.00)
     - energy 0.40 vs target 0.40 (+1.50)
     - acousticness 0.78 vs target 0.80 (+0.98)
     - valence 0.59 vs target 0.60 (+0.49)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.68 / 6.00   [ambient, chill]
   Reasons:
     - mood match: chill (+1.00)
     - energy 0.28 vs target 0.40 (+1.32)
     - acousticness 0.92 vs target 0.80 (+0.88)
     - valence 0.65 vs target 0.60 (+0.47)

5. Coffee Shop Stories by Slow Stereo
   Score: 2.81 / 6.00   [jazz, relaxed]
   Reasons:
     - energy 0.37 vs target 0.40 (+1.46)
     - acousticness 0.89 vs target 0.80 (+0.91)
     - valence 0.71 vs target 0.60 (+0.45)
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



