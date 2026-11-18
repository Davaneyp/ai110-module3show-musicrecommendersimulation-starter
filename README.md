# 🎵 Music Recommender Simulation

## Project Summary

My version is **TuneJudge 1.0**, a content-based recommender that picks the top 5 songs from a 20-song catalog for a listener. The listener gives a favorite genre, a favorite mood, and target levels for energy, valence (how positive the music sounds), and acousticness. TuneJudge gives every song points for how well it matches, ranks the songs from highest to lowest, and lists the reasons behind each score. I tested it with 3 typical listeners and 7 tricky profiles, and I ran one experiment that changed the weights. Those tests showed where it works well and where it is biased: genre and mood labels can outweigh how a song actually sounds, and listeners whose favorite genre has only one song in the catalog get weaker recommendations. The full write-up is in the [Model Card](model_card.md).

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
   ```

2. Install dependencies:

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

Here is the output for the first two profiles, Happy Pop and Chill Lofi, from `python -m src.main`. The other 8 profiles are in the [Model Card, Section 7](model_card.md#7-evaluation).

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

---

## Stress Test: Diverse and Adversarial Profiles

I ran the recommender on 3 standard profiles and 7 adversarial or edge-case profiles (conflicting preferences, unknown labels, messy input, out-of-range values, and an empty profile). The full terminal output and observations are in the [Model Card, Section 7: Evaluation](model_card.md#7-evaluation).

---

## Experiments You Tried

- **Weight Shift (energy ×2, genre ×½):** Toggle with `EXPERIMENT_WEIGHT_SHIFT` in `src/recommender.py`. It fixed some label-over-sound mistakes (Happy Pop, Sad but Hyped) but made genre nearly irrelevant. See the [Model Card, Section 7](model_card.md#7-evaluation) for the full comparison.
- **Adding valence to the score:** The starter profile had no valence. I added it (worth up to 0.5 points) so the recommender could tell apart songs with similar energy but a different feel, like a cheerful song versus a dark one. Because it is the smallest weight, it mostly breaks close ties and rarely changes which songs make the top 5.
- **Different types of users:** I ran 3 typical listeners and 7 tricky profiles. Typical tastes got near-perfect #1 picks (5.87 to 5.94 out of 6). Tricky profiles exposed problems: a sad, high-energy listener got a quiet acoustic folk song at #1, and an empty profile still got a "top 5" made of the first five songs in the file.

---

## Limitations and Risks

- **Tiny, made-up catalog.** There are only 20 songs, and their numbers were invented, not measured from real audio.
- **Uneven genres.** Lofi has 3 songs and pop has 2, but the other 15 genres have 1 song each. A lofi fan gets a list full of lofi, while a classical or metal fan gets one real match and then leftovers.
- **Labels can beat sound.** A genre and mood match is worth 3 of the 6 points. A listener who asked for loud, high-energy music got a quiet acoustic folk song at #1, only because it was tagged "folk" and "sad."
- **Exact label matching only.** "indie pop" gets no credit for a pop fan, and "relaxed" gets none for a chill fan, even though they are close in meaning.
- **No guardrails.** Unknown genres, impossible numbers like energy 1.5, and an empty profile all still return a confident-looking top 5 with no warning.
- **The same songs keep showing up.** Gym Hero appeared in 7 of the 10 test lists, because it is close to any listener who wants energetic music.
- **Missing information.** It does not use lyrics, language, artist, release year, or what the user has listened to before.

See [Model Card, Section 6](model_card.md#6-limitations-and-bias) for more detail.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building TuneJudge showed me that a recommender doesn't "understand" music. It just turns preferences into numbers and adds them up. Every song gets points for matching the user's genre and mood, plus points for how close its energy, valence, and acousticness are to what the user asked for. Then the songs are sorted by score. That simple recipe worked well for clear, typical tastes like Happy Pop or Chill Lofi, where the #1 pick was almost perfect. But I learned that the weights decide everything. When I doubled energy and halved genre, some rankings got better and others got worse, and the classical fan lost their only classical song. There isn't one "correct" set of weights. Every choice favors some listeners over others.

I also saw how bias can come from the data, not just the code. Lofi had three songs in the catalog, while most genres had only one, so a lofi fan got a full list of lofi and a metal or folk fan got one real match and then leftovers. Exact label matching made it worse, since "indie pop" got no credit for a pop fan. The system also never admits when it doesn't know something. An empty profile still got a confident "top 5." In a real app with millions of users, these same problems could keep pushing popular genres and the same few songs while people with less common tastes get worse recommendations without realizing it.


