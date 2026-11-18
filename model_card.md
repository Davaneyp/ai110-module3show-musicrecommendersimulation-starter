# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneJudge 1.0**

It works like a judge at a contest. Every song gets points for how well it fits you, and the highest scores win.

---

## 2. Intended Use  

**Goal / task:** TuneJudge suggests the top 5 songs from a small catalog that best fit one listener's taste. It does not predict ratings or learn from plays. It only compares song features to what the user says they like.

**What it assumes about the user:**

- They can name one favorite genre and one favorite mood.
- They can describe the sound they want with numbers from 0 to 1: energy, positivity (valence), and how acoustic it is.
- Their taste stays the same for the whole session.

**Intended use:**

- Classroom learning about how recommenders turn data into rankings.
- Testing how scoring weights create bias.
- Showing the reasons behind each pick, so the logic is easy to inspect.

**Not intended for:**

- Real users or a real music app. The catalog is 20 made-up songs.
- Judging what music is "good." A high score only means "close to what you typed."
- Any decision with real stakes, like paying artists or deciding which songs get promoted.
- Users who don't know their own preferences. An empty or unknown profile still gets a confident-looking list, which is misleading.

---

## 3. How the Model Works  

TuneJudge looks at five things about each song and gives it points:

- **Genre match: 2 points.** The song's genre is exactly your favorite genre.
- **Mood match: 1 point.** The song's mood is exactly your favorite mood.
- **Energy: up to 1.5 points.** The closer the song's energy is to what you asked for, the more points. A perfect match gets all 1.5.
- **Acousticness: up to 1 point.** Same idea. Closer to your target means more points.
- **Valence (how happy it sounds): up to 0.5 points.** Same idea again.

The best possible score is 6 points. TuneJudge scores every song, sorts them from highest to lowest, and shows the top 5. Each pick comes with a list of reasons, like "genre match: pop (+2.00)."

Genre is worth the most because it reflects long-term taste. Mood changes with the moment, so it is worth less. Energy counts by *closeness*, not by size, so someone who wants calm music doesn't get handed the loudest song.

**Changes from the starter logic:**

- Built the scoring and ranking from scratch (the starter only returned the first 5 songs).
- Added valence and a numeric acousticness target to the profile.
- Made label matching ignore capital letters and extra spaces, so "  POP " still matches "pop."
- Show every point a song earned, so each recommendation explains itself.
- Added a switch to test a different set of weights (see Section 7).

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. The starter had 10. I added 10 more to cover more genres and moods.
- **Features per song:** title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The numbers run from 0 to 1, except tempo, which is in beats per minute.
- **Features used in scoring:** genre, mood, energy, valence, and acousticness. Tempo and danceability are left out because they mostly rise and fall with energy.
- **Genres:** 17. Lofi has 3 songs, pop has 2, and the other 15 genres (rock, jazz, metal, classical, folk, and more) have 1 song each.
- **Moods:** 16. Chill has 3 songs, happy and intense have 2 each, and the rest have 1.

**Limits:**

- The songs and numbers are made up. They were not measured from real audio.
- Most genres have only one song, so many users get one real match and then leftovers.
- There are no lyrics, language, release year, artist popularity, or listening history.
- Each song has exactly one genre and one mood. Real songs often fit several.
- Genre and mood labels mostly reflect Western popular music.

---

## 5. Strengths  

- **Clear, typical tastes work well.** Happy Pop, Chill Lofi, and Deep Intense Rock each got a near-perfect #1 (5.87 to 5.94 out of 6), and the rest of each list sounded like the same vibe.
- **Energy really controls the feel.** Chill Lofi and Deep Intense Rock shared zero songs. The quiet profile got quiet songs, and the loud one got loud songs.
- **Messy typing doesn't break it.** "  POP " and "Happy" gave the exact same list as "pop" and "happy."
- **Every pick explains itself.** You can see exactly where each point came from, which made the biases easy to find.
- **It is easy to tune.** All the weights live in one place, so you can change them without touching the ranking code.

---

## 6. Limitations and Bias 

**Main weakness: genre imbalance creates a filter bubble for some users and a near-random list for others.** The catalog has 17 genres, but lofi has 3 songs and pop has 2, while the other 15 genres have exactly one song each. Because a genre match is worth +2.0 (a third of the maximum score), a lofi fan can fill three of their five recommendations with genre matches, and the Chill Lofi results stay tightly inside that one sound. A classical, folk, or metal fan gets one genre match at most, and the other four slots are filled by whichever songs happen to have a similar energy, so the same high-energy tracks (Gym Hero, Concrete Crown, Storm Runner) keep showing up for very different users. In practice, the system serves users with well-represented tastes well and gives everyone else one real match followed by leftovers.

**Other biases found during testing:**

- **The energy gap favors middle-energy users.** Energy points are `1.5 × (1 − gap)`, and catalog energies range from 0.22 to 0.98. A user who targets 0.5 earns at least 0.78 energy points from every song, while a user who wants very quiet music (target 0.1) averages only 0.74 points, and no song falls within 0.1 of that target.
- **Labels can override sound.** A genre and mood match (+3.0 together) put a quiet acoustic folk song at #1 for a user who asked for energy 0.9 (Sad but Hyped profile).
- **Exact label matching.** "indie pop" gets no credit for a "pop" fan, and "relaxed" or "focused" get no credit for a "chill" fan, even though they are close in meaning.
- **No guardrails on input.** Unknown genres, out-of-range targets, and an empty profile all return a confident-looking top 5 with no warning.

---

## 7. Evaluation  

**How I tested it, in short:**

- Ran 10 user profiles through `python -m src.main`: 3 typical listeners and 7 tricky ones.
- Read each top 5 and asked, "Would this person actually want these songs?"
- Compared pairs of profiles that differ in one or two settings to see what each setting really does.
- Ran one weight experiment (energy doubled, genre halved) and compared it to the baseline.
- No accuracy metrics. The checks were by reading the results and the reasons.

### Profiles Tested

I tested 10 user profiles: 3 typical listeners and 7 profiles designed to trick the scoring.

| Profile | What it tests |
|---|---|
| Happy Pop | Typical upbeat listener (baseline) |
| Chill Lofi | Typical quiet, acoustic listener (baseline) |
| Deep Intense Rock | Typical loud, aggressive listener (baseline) |
| Sad but Hyped | Conflicting wishes: a sad mood but very high energy |
| Euphoric Classical | Favorite genre disagrees with the requested sound |
| Ghost Genre | Genre and mood that do not exist in the catalog |
| Messy Labels | Same as Happy Pop, but typed as `"  POP "` and `"Happy"` |
| Out of Range | Impossible numbers (energy 1.5, acousticness -0.5) |
| Dead Center | No genre or mood, every number set to the middle (0.5) |
| Empty Profile | No preferences at all |

### What Surprised Me

- **A song's label can beat how it sounds.** The Sad but Hyped user asked for loud, high-energy music but got a quiet acoustic folk song at #1, only because it was tagged "folk" and "sad."
- **The favorite genre does not always win.** The Euphoric Classical user's only classical song fell to #4. An EDM song that matched the mood and the sound came first.
- **The system never says "I don't know."** With no preferences at all, it still returned a top 5. Every song scored 0.00, so the list was just the first five songs in the file.
- **The same few songs keep coming back.** Gym Hero appeared in 7 of the 10 top-5 lists, and Concrete Crown in 6.

### Why "Gym Hero" Keeps Showing Up for Happy Pop Fans

Think of the recommender as a judge handing out points. The biggest prize, 2 points, goes to any song filed under the listener's favorite genre. Gym Hero is filed under "pop," so it collects that prize right away. Rooftop Lights is a happier song that sounds closer to what the listener wants, but it is filed under "indie pop," and the judge only gives the prize for an exact name match, so it gets nothing. Gym Hero's mood is "intense," not "happy," but a mood match is only worth 1 point, so missing it costs less than the genre prize is worth. Gym Hero is also loud and electronic, which is close to the energy and sound the Happy Pop listener asked for. Add it up and a workout song lands at #2 for someone who wanted cheerful pop (4.64 points against 3.79 for Rooftop Lights).

The same thing explains why Gym Hero shows up almost everywhere. It is very high energy and barely acoustic, so it is a close numeric match for any listener who wants energetic music. Its "pop" and "intense" labels also earn bonus points for two of the profiles.

### Profile Comparisons

Each pair below differs in one or two important ways, so the change in output shows what that preference actually does.

- **Happy Pop vs. Chill Lofi:** The two lists share no songs at all. Happy Pop gets bright, loud, electronic songs (energy around 0.8), and Chill Lofi gets quiet, acoustic study music (energy around 0.4). This makes sense because the two profiles disagree on every setting.
- **Happy Pop vs. Deep Intense Rock:** Both want high energy and low acousticness, so they share Gym Hero and Concrete Crown. The difference is at the top: Happy Pop's #1 is the cheerful Sunrise City, while Rock's #1 is Storm Runner, and Rock pulls in the dark, angry metal song Iron Tempest. That fits, because Rock asked for a low positivity score (valence 0.40) and Happy Pop asked for a high one (0.80).
- **Chill Lofi vs. Deep Intense Rock:** No overlap. Lofi's songs are all below 0.45 energy and Rock's are all 0.75 or higher. This is the clearest sign that the energy setting really controls the "loudness" of the list.
- **Deep Intense Rock vs. Sad but Hyped:** These two lists share four of five songs, because both ask for energy around 0.9 and very low acousticness. The only difference is #1: Sad but Hyped puts the quiet folk song Hollow Pines first because it matches the "folk" and "sad" labels. This shows the label bonuses can override the numbers for exactly one slot, and the numbers decide the rest.
- **Happy Pop vs. Messy Labels:** The outputs are identical. Odd capitalization and extra spaces in the genre and mood do not confuse the matching, which is the result we wanted.
- **Happy Pop vs. Ghost Genre:** The number settings are similar (energy 0.7 to 0.8, low acousticness), so both lists include Rooftop Lights, Fuego Lento, and Concrete Crown. But without a real genre or mood to match, Sunrise City and Gym Hero drop out completely, and every score lands between 2.65 and 2.80. Without labels, the recommender has very little to separate songs, so the order is close to a coin flip.
- **Euphoric Classical vs. Happy Pop:** Both lists include Gym Hero and Sunrise City because both want upbeat, high-energy songs. The classical fan's only classical song barely makes the list at #4, which shows that when a favorite genre clashes with the requested sound, the sound usually wins.
- **Deep Intense Rock vs. Out of Range:** Both point toward loud, heavy music, and Iron Tempest (metal, angry) wins Out of Range by a huge margin (4.57 against 1.28 for #2). The impossible targets squash every other score toward zero. The ranking still looks reasonable, but the system never warns that energy 1.5 is not a real value.
- **Chill Lofi vs. Dead Center:** They share only Midnight Coding. Dead Center has no genre or mood, so it favors songs that are "medium" on every scale, like R&B, reggae, country, and blues. Chill Lofi leans toward the quiet, acoustic end. This shows that a middle-of-the-road profile gets middle-of-the-road music, not a mix of everything.
- **Dead Center vs. Empty Profile:** Dead Center at least has numbers to compare, so it produces a sensible ranking. The Empty Profile has nothing, so every song ties at 0.00 and the list is just catalog order. A real app should ask for preferences instead of pretending to recommend.

### Stress Test Output

Run with `python -m src.main`. The first three profiles are typical listeners. The rest are adversarial or edge-case profiles, built to test whether the scoring logic can be tricked (conflicting preferences, unknown labels, messy input, out-of-range values, and empty input). Each block below is the real terminal output showing the top 5 results.

### Standard Profiles

#### Happy Pop

```text
================================================================
Profile: Happy Pop
  genre='pop', mood='happy', energy=0.80, valence=0.80, acousticness=0.20
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
```

*Observation:* Baseline. Works as intended: the one pop + happy song wins by a wide margin.

#### Chill Lofi

```text
================================================================
Profile: Chill Lofi
  genre='lofi', mood='chill', energy=0.40, valence=0.60, acousticness=0.80
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

*Observation:* Baseline. Both lofi + chill songs score within 0.01 of each other, and the lofi + focused song takes #3.

#### Deep Intense Rock

```text
================================================================
Profile: Deep Intense Rock
  genre='rock', mood='intense', energy=0.90, valence=0.40, acousticness=0.10
================================================================
1. Storm Runner by Voltline
   Score: 5.94 / 6.00   [rock, intense]
   Reasons:
     - genre match: rock (+2.00)
     - mood match: intense (+1.00)
     - energy 0.91 vs target 0.90 (+1.48)
     - acousticness 0.10 vs target 0.10 (+1.00)
     - valence 0.48 vs target 0.40 (+0.46)

2. Gym Hero by Max Pulse
   Score: 3.72 / 6.00   [pop, intense]
   Reasons:
     - mood match: intense (+1.00)
     - energy 0.93 vs target 0.90 (+1.46)
     - acousticness 0.05 vs target 0.10 (+0.95)
     - valence 0.77 vs target 0.40 (+0.32)

3. Iron Tempest by Grave Signal
   Score: 2.73 / 6.00   [metal, angry]
   Reasons:
     - energy 0.98 vs target 0.90 (+1.38)
     - acousticness 0.04 vs target 0.10 (+0.94)
     - valence 0.21 vs target 0.40 (+0.40)

4. Concrete Crown by Kilo Verse
   Score: 2.69 / 6.00   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 0.90 (+1.32)
     - acousticness 0.12 vs target 0.10 (+0.98)
     - valence 0.62 vs target 0.40 (+0.39)

5. Night Drive Loop by Neon Echo
   Score: 2.61 / 6.00   [synthwave, moody]
   Reasons:
     - energy 0.75 vs target 0.90 (+1.27)
     - acousticness 0.22 vs target 0.10 (+0.88)
     - valence 0.49 vs target 0.40 (+0.46)
```

*Observation:* Baseline. Storm Runner is a near-perfect match (5.94). Gym Hero, a *pop* song, takes #2 only because its mood label is "intense". Iron Tempest (metal) fits the sound better but has no label match, so it lands at #3.

### Adversarial / Edge-Case Profiles

#### Conflict: Sad but Hyped

```text
================================================================
Profile: Conflict: Sad but Hyped
  genre='folk', mood='sad', energy=0.90, valence=0.20, acousticness=0.10
================================================================
1. Hollow Pines by Ember & Ash
   Score: 4.26 / 6.00   [folk, sad]
   Reasons:
     - genre match: folk (+2.00)
     - mood match: sad (+1.00)
     - energy 0.30 vs target 0.90 (+0.60)
     - acousticness 0.91 vs target 0.10 (+0.19)
     - valence 0.25 vs target 0.20 (+0.47)

2. Storm Runner by Voltline
   Score: 2.84 / 6.00   [rock, intense]
   Reasons:
     - energy 0.91 vs target 0.90 (+1.48)
     - acousticness 0.10 vs target 0.10 (+1.00)
     - valence 0.48 vs target 0.20 (+0.36)

3. Iron Tempest by Grave Signal
   Score: 2.82 / 6.00   [metal, angry]
   Reasons:
     - energy 0.98 vs target 0.90 (+1.38)
     - acousticness 0.04 vs target 0.10 (+0.94)
     - valence 0.21 vs target 0.20 (+0.49)

4. Gym Hero by Max Pulse
   Score: 2.62 / 6.00   [pop, intense]
   Reasons:
     - energy 0.93 vs target 0.90 (+1.46)
     - acousticness 0.05 vs target 0.10 (+0.95)
     - valence 0.77 vs target 0.20 (+0.21)

5. Concrete Crown by Kilo Verse
   Score: 2.59 / 6.00   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 0.90 (+1.32)
     - acousticness 0.12 vs target 0.10 (+0.98)
     - valence 0.62 vs target 0.20 (+0.29)
```

*Observation:* **Tricked.** The user asked for high energy (0.90) and low acousticness (0.10), but the top pick is a quiet acoustic folk song (energy 0.30, acousticness 0.91). The +3.0 from matching genre and mood outweighs the two features it badly misses. Songs #2 to #5 fit the requested *sound* much better.

#### Conflict: Euphoric Classical

```text
================================================================
Profile: Conflict: Euphoric Classical
  genre='classical', mood='euphoric', energy=0.95, valence=0.90, acousticness=0.05
================================================================
1. Pulse Horizon by Vanta Drop
   Score: 3.96 / 6.00   [edm, euphoric]
   Reasons:
     - mood match: euphoric (+1.00)
     - energy 0.96 vs target 0.95 (+1.48)
     - acousticness 0.03 vs target 0.05 (+0.98)
     - valence 0.88 vs target 0.90 (+0.49)

2. Gym Hero by Max Pulse
   Score: 2.91 / 6.00   [pop, intense]
   Reasons:
     - energy 0.93 vs target 0.95 (+1.47)
     - acousticness 0.05 vs target 0.05 (+1.00)
     - valence 0.77 vs target 0.90 (+0.43)

3. Storm Runner by Voltline
   Score: 2.68 / 6.00   [rock, intense]
   Reasons:
     - energy 0.91 vs target 0.95 (+1.44)
     - acousticness 0.10 vs target 0.05 (+0.95)
     - valence 0.48 vs target 0.90 (+0.29)

4. Moonlit Sonata Reimagined by Clara Vey
   Score: 2.68 / 6.00   [classical, melancholy]
   Reasons:
     - genre match: classical (+2.00)
     - energy 0.22 vs target 0.95 (+0.41)
     - acousticness 0.97 vs target 0.05 (+0.08)
     - valence 0.28 vs target 0.90 (+0.19)

5. Sunrise City by Neon Echo
   Score: 2.64 / 6.00   [pop, happy]
   Reasons:
     - energy 0.82 vs target 0.95 (+1.30)
     - acousticness 0.18 vs target 0.05 (+0.87)
     - valence 0.84 vs target 0.90 (+0.47)
```

*Observation:* The genre bonus **loses** here. The only classical song falls to #4 (2.68), tied with Storm Runner. An EDM track with the right mood and near-perfect numbers wins instead. When genre and audio features disagree, mood plus the numeric features (up to 4.0) can beat genre (2.0).

#### Ghost Genre (k-pop / dreamy)

```text
================================================================
Profile: Ghost Genre (k-pop / dreamy)
  genre='k-pop', mood='dreamy', energy=0.70, valence=0.70, acousticness=0.30
================================================================
1. Rooftop Lights by Indigo Parade
   Score: 2.80 / 6.00   [indie pop, happy]
   Reasons:
     - energy 0.76 vs target 0.70 (+1.41)
     - acousticness 0.35 vs target 0.30 (+0.95)
     - valence 0.81 vs target 0.70 (+0.44)

2. Night Drive Loop by Neon Echo
   Score: 2.74 / 6.00   [synthwave, moody]
   Reasons:
     - energy 0.75 vs target 0.70 (+1.42)
     - acousticness 0.22 vs target 0.30 (+0.92)
     - valence 0.49 vs target 0.70 (+0.40)

3. Fuego Lento by Sol Marea
   Score: 2.73 / 6.00   [latin, playful]
   Reasons:
     - energy 0.81 vs target 0.70 (+1.33)
     - acousticness 0.30 vs target 0.30 (+1.00)
     - valence 0.90 vs target 0.70 (+0.40)

4. Concrete Crown by Kilo Verse
   Score: 2.66 / 6.00   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 0.70 (+1.38)
     - acousticness 0.12 vs target 0.30 (+0.82)
     - valence 0.62 vs target 0.70 (+0.46)

5. Velvet Hours by Amara Lane
   Score: 2.65 / 6.00   [r&b, romantic]
   Reasons:
     - energy 0.52 vs target 0.70 (+1.23)
     - acousticness 0.38 vs target 0.30 (+0.92)
     - valence 0.70 vs target 0.70 (+0.50)
```

*Observation:* Neither label exists in the catalog, so the max reachable score is 3.0. All five results sit within 0.15 of each other, so the ranking is close to arbitrary, and the user gets no warning that their genre and mood were never found.

#### Messy Labels ('  POP ', 'Happy')

```text
================================================================
Profile: Messy Labels ('  POP ', 'Happy')
  genre='  POP ', mood='Happy', energy=0.80, valence=0.80, acousticness=0.20
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
```

*Observation:* Passed. Output is identical to Happy Pop, so case-insensitive, whitespace-stripped label matching works.

#### Out of Range (energy 1.5, acoustic -0.5)

```text
================================================================
Profile: Out of Range (energy 1.5, acoustic -0.5)
  genre='metal', mood='angry', energy=1.50, valence=0.00, acousticness=-0.50
================================================================
1. Iron Tempest by Grave Signal
   Score: 4.57 / 6.00   [metal, angry]
   Reasons:
     - genre match: metal (+2.00)
     - mood match: angry (+1.00)
     - energy 0.98 vs target 1.50 (+0.72)
     - acousticness 0.04 vs target -0.50 (+0.46)
     - valence 0.21 vs target 0.00 (+0.40)

2. Storm Runner by Voltline
   Score: 1.28 / 6.00   [rock, intense]
   Reasons:
     - energy 0.91 vs target 1.50 (+0.61)
     - acousticness 0.10 vs target -0.50 (+0.40)
     - valence 0.48 vs target 0.00 (+0.26)

3. Pulse Horizon by Vanta Drop
   Score: 1.22 / 6.00   [edm, euphoric]
   Reasons:
     - energy 0.96 vs target 1.50 (+0.69)
     - acousticness 0.03 vs target -0.50 (+0.47)
     - valence 0.88 vs target 0.00 (+0.06)

4. Gym Hero by Max Pulse
   Score: 1.21 / 6.00   [pop, intense]
   Reasons:
     - energy 0.93 vs target 1.50 (+0.65)
     - acousticness 0.05 vs target -0.50 (+0.45)
     - valence 0.77 vs target 0.00 (+0.11)

5. Concrete Crown by Kilo Verse
   Score: 0.99 / 6.00   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 1.50 (+0.42)
     - acousticness 0.12 vs target -0.50 (+0.38)
     - valence 0.62 vs target 0.00 (+0.19)
```

*Observation:* No input validation. Targets outside 0 to 1 are accepted silently. The ranking still looks reasonable, but scores are squashed (the best metal song gets only +0.72 energy). A target far enough out (for example energy 3.0) would make the closeness terms **negative** and subtract points.

#### Dead Center (all 0.5, no labels)

```text
================================================================
Profile: Dead Center (all 0.5, no labels)
  genre=None, mood=None, energy=0.50, valence=0.50, acousticness=0.50
================================================================
1. Velvet Hours by Amara Lane
   Score: 2.75 / 6.00   [r&b, romantic]
   Reasons:
     - energy 0.52 vs target 0.50 (+1.47)
     - acousticness 0.38 vs target 0.50 (+0.88)
     - valence 0.70 vs target 0.50 (+0.40)

2. Midnight Coding by LoRoom
   Score: 2.64 / 6.00   [lofi, chill]
   Reasons:
     - energy 0.42 vs target 0.50 (+1.38)
     - acousticness 0.71 vs target 0.50 (+0.79)
     - valence 0.56 vs target 0.50 (+0.47)

3. Island Time by Roots Harbor
   Score: 2.62 / 6.00   [reggae, uplifting]
   Reasons:
     - energy 0.60 vs target 0.50 (+1.35)
     - acousticness 0.45 vs target 0.50 (+0.95)
     - valence 0.85 vs target 0.50 (+0.33)

4. Dusty Back Roads by Hank Willow
   Score: 2.59 / 6.00   [country, nostalgic]
   Reasons:
     - energy 0.55 vs target 0.50 (+1.42)
     - acousticness 0.74 vs target 0.50 (+0.76)
     - valence 0.68 vs target 0.50 (+0.41)

5. Crossroads Blues by Willie Delta
   Score: 2.59 / 6.00   [blues, soulful]
   Reasons:
     - energy 0.46 vs target 0.50 (+1.44)
     - acousticness 0.80 vs target 0.50 (+0.70)
     - valence 0.40 vs target 0.50 (+0.45)
```

*Observation:* With no labels, "middle of the road" songs (R&B, lofi, reggae, country, blues) win. Extreme tracks like metal and EDM can never rank highly for a neutral user.

#### Empty Profile

```text
================================================================
Profile: Empty Profile
  genre=None, mood=None
================================================================
1. Sunrise City by Neon Echo
   Score: 0.00 / 6.00   [pop, happy]
   Reasons:
     - (no preferences matched)

2. Midnight Coding by LoRoom
   Score: 0.00 / 6.00   [lofi, chill]
   Reasons:
     - (no preferences matched)

3. Storm Runner by Voltline
   Score: 0.00 / 6.00   [rock, intense]
   Reasons:
     - (no preferences matched)

4. Library Rain by Paper Lanterns
   Score: 0.00 / 6.00   [lofi, chill]
   Reasons:
     - (no preferences matched)

5. Gym Hero by Max Pulse
   Score: 0.00 / 6.00   [pop, intense]
   Reasons:
     - (no preferences matched)
```

*Observation:* **Tricked.** With no preferences, every song scores 0.00, and the system still returns a "top 5". That list is just catalog order from the stable sort tie-break. It should return nothing or ask for preferences.

### Takeaways

- **Labels can override sound.** A genre plus mood match (+3.0) can push a song to #1 even when its energy and acousticness are the opposite of what the user asked for (Sad but Hyped).
- **Genre is not always decisive.** When every numeric feature disagrees with the favorite genre, a mood match plus close audio features can beat it (Euphoric Classical).
- **No guardrails on input.** Unknown labels, out-of-range targets, and empty profiles all produce confident-looking top-5 lists with no warning.
- **Normalization works.** Casing and whitespace in labels do not break matching.

### Experiment: Weight Shift (energy ×2, genre ×½)

**Change:** In `src/recommender.py`, setting `EXPERIMENT_WEIGHT_SHIFT = True` changes `ENERGY_WEIGHT` from 1.5 to 3.0 and `GENRE_WEIGHT` from 2.0 to 1.0. Mood, acousticness, and valence weights are unchanged.

**Math check:** The maximum score rises from 6.0 to **6.5** (1.0 + 1.0 + 3.0 + 1.0 + 0.5). `MAX_SCORE` is now calculated from the weights, so the output shows `/ 6.50` instead of the hard-coded `/ 6.00`. Each closeness term still stays between 0 and its weight when targets are between 0 and 1. With the switch set back to `False`, the output matches the original baseline exactly.

**Top-5 comparison (baseline → experiment):**

| Profile | Baseline top 3 | Weight Shift top 3 | What changed |
|---|---|---|---|
| Happy Pop | Sunrise City, Gym Hero, Rooftop Lights | Sunrise City, **Rooftop Lights**, Gym Hero | Happy indie pop now beats intense workout pop |
| Chill Lofi | Library Rain, Midnight Coding, Focus Flow | **Midnight Coding**, Library Rain, Focus Flow | #1 and #2 swap (gap of 0.04) |
| Deep Intense Rock | Storm Runner, Gym Hero, Iron Tempest | Same | #5 Night Drive Loop → Pulse Horizon |
| Sad but Hyped | **Hollow Pines**, Storm Runner, Iron Tempest | **Storm Runner**, Iron Tempest, Gym Hero | Quiet folk song drops out of the top 5 entirely |
| Euphoric Classical | Pulse Horizon, Gym Hero, Storm Runner (#4 Moonlit Sonata) | Pulse Horizon, Gym Hero, Storm Runner | The only classical song drops out of the top 5 |
| Ghost Genre | Rooftop Lights, Night Drive Loop, Fuego Lento | Same | #5 Velvet Hours → Island Time |
| Out of Range | Iron Tempest, Storm Runner, Pulse Horizon | Iron Tempest, Pulse Horizon, Storm Runner | #2 and #3 swap |
| Dead Center | Velvet Hours, Midnight Coding, Island Time | Velvet Hours, Crossroads Blues, Midnight Coding | Middle of the list reshuffles |
| Empty Profile | Catalog order | Catalog order | No change (all scores still 0.00) |

Terminal output for the profile that changed most:

```text
================================================================
Profile: Conflict: Sad but Hyped
  genre='folk', mood='sad', energy=0.90, valence=0.20, acousticness=0.10
================================================================
1. Storm Runner by Voltline
   Score: 4.33 / 6.50   [rock, intense]
   Reasons:
     - energy 0.91 vs target 0.90 (+2.97)
     - acousticness 0.10 vs target 0.10 (+1.00)
     - valence 0.48 vs target 0.20 (+0.36)

2. Iron Tempest by Grave Signal
   Score: 4.20 / 6.50   [metal, angry]
   Reasons:
     - energy 0.98 vs target 0.90 (+2.76)
     - acousticness 0.04 vs target 0.10 (+0.94)
     - valence 0.21 vs target 0.20 (+0.49)

3. Gym Hero by Max Pulse
   Score: 4.08 / 6.50   [pop, intense]
   Reasons:
     - energy 0.93 vs target 0.90 (+2.91)
     - acousticness 0.05 vs target 0.10 (+0.95)
     - valence 0.77 vs target 0.20 (+0.21)

4. Concrete Crown by Kilo Verse
   Score: 3.91 / 6.50   [hip-hop, confident]
   Reasons:
     - energy 0.78 vs target 0.90 (+2.64)
     - acousticness 0.12 vs target 0.10 (+0.98)
     - valence 0.62 vs target 0.20 (+0.29)

5. Pulse Horizon by Vanta Drop
   Score: 3.91 / 6.50   [edm, euphoric]
   Reasons:
     - energy 0.96 vs target 0.90 (+2.82)
     - acousticness 0.03 vs target 0.10 (+0.93)
     - valence 0.88 vs target 0.20 (+0.16)
```

**More accurate or just different?**

- **More accurate** where the labels and the sound disagreed. Happy Pop now ranks the happy song at #2 over an intense one, and Sad but Hyped now returns high-energy songs, which is what the user's numbers asked for.
- **Just different** for most other profiles. Chill Lofi, Ghost Genre, Out of Range, and Dead Center only swapped songs that were already within about 0.1 points of each other.
- **Worse in one way.** Energy is now nearly half the maximum score (3.0 of 6.5), so genre barely matters. The Euphoric Classical user gets **no classical music at all**, and lists lean even harder toward the same high-energy songs (Gym Hero, Storm Runner, Concrete Crown).

The experiment shows the rankings are very sensitive to the weights. It doesn't fix the system so much as trade one bias (labels over sound) for another (energy over everything else). The baseline weights were restored after the experiment.

---

## 8. Future Work  

1. **Give partial credit for similar labels.** "indie pop" should earn some points for a pop fan, and "relaxed" or "focused" should earn some for a chill fan. A simple table of related genres and moods would do it.
2. **Add guardrails.** Keep targets between 0 and 1. Warn the user when their genre or mood isn't in the catalog. Ask for preferences instead of returning a list when the profile is empty.
3. **Add variety to the top 5.** Limit how many songs from one genre can appear, and lower the score of songs that already show up everywhere (like Gym Hero), so users see more of the catalog.

A bigger, more balanced catalog would also help, so every genre has more than one song.

---

## 9. Personal Reflection  

A few sentences about your experience.  

What I learned about recommender systems: A recommender is really a set of choices about what matters. Picking how many points genre is worth compared to energy decides what every user sees. Small weight changes can reshuffle the whole list.

Something unexpected: I was surprised how often a song's label beat how it actually sounds. The Sad but Hyped listener asked for loud, high-energy music and got a quiet acoustic folk song at #1, just because it was tagged "folk" and "sad." I was also surprised that Gym Hero showed up in 7 of my 10 test lists. One song that sits close to "energetic" can take over the results for a lot of different people.

How this changed how I think about music apps: When an app like Spotify recommends something, I now wonder what it's weighing and who it might be leaving out (Especially with their AI playlist creation feature, sometimes some of the songs in the playlist don't match my description). If my 20-song system already has a filter bubble, a real app could too. I'd want recommendations that explain themselves, mix in some variety, and say "I'm not sure" when they don't have enough information about me.

