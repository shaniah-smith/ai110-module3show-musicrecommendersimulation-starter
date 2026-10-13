# 🎵 Music Recommender Simulation

## Project Summary

This project is a small **content-based music recommender** written in Python. It reads a catalog of 18 songs from `data/songs.csv`, compares each song to a user's "taste profile" (favorite mood, favorite genre, target energy, and whether they like acoustic music), gives every song a score with a list of reasons, and returns the top 5. The goal is to understand, and explain, how apps like Spotify turn data into "you might like this," and where that process can go wrong.

---

## How The System Works

### How real recommenders work

Real platforms like Spotify and YouTube mostly combine two ideas. **Collaborative filtering** looks at other people's behavior: if listeners who like the same songs as you also play song X, you'll probably like song X too. It uses likes, skips, replays, playlist adds, and listening time. **Content-based filtering** looks at the songs themselves (genre, mood, tempo, energy, acousticness) and finds songs that are similar to what you already like. Collaborative filtering is great at surprising discoveries but can't recommend a brand-new song nobody has played yet. Content-based filtering works for any song but tends to keep giving you more of the same.

**My version is content-based only**, because there are no other users in this simulation, just song attributes. It prioritizes **mood first**, because to me the feeling of a song matters more than the label on it. Then it looks at genre, then how close the energy is.

### Features used

**`Song`:** `genre`, `mood`, `energy` (0–1), and `acousticness` (0–1) are used in scoring. `title`, `artist`, `tempo_bpm`, `valence`, and `danceability` are stored but not scored.

**`UserProfile`:** `favorite_mood`, `favorite_genre`, `target_energy` (0–1), and `likes_acoustic` (True/False).

### Algorithm Recipe

| Rule | Points | Why |
|---|---|---|
| Mood matches | **+2.0** | The feeling of a song is the strongest signal of what the listener wants right now |
| Genre matches | **+1.0** | Helpful, but moods cross genres (lofi and ambient can both be "chill") |
| Energy closeness | **0 to +1.0**, `1 − |song energy − target energy|` | Rewards songs *close* to the target, not just high or low energy |
| Acoustic fit | **0 to +0.5** | `acousticness` if the user likes acoustic music, otherwise `1 − acousticness` |

Highest possible score: **4.5**.

- **Scoring rule** (`score_song`): judges one song and returns `(score, reasons)`.
- **Ranking rule** (`recommend_songs`): scores every song, sorts from highest to lowest, and keeps the top `k`.

### Data flow

```
User prefs ──► for each song in songs.csv ──► score_song() ──► (score, reasons)
                                                                     │
                       Top K recommendations ◄── sort high → low ◄───┘
```

### Expected biases

- Because mood is worth the most, the system may recommend a song with the right mood but the **wrong energy** over a song with the right energy but a slightly different mood.
- Genres and moods are matched **exactly**, so "indie pop" gets no credit from a "pop" fan.
- The catalog is tiny (18 songs, and most moods have only 1–2 songs), so after the first couple of matches the list fills up with songs that only score on energy.

---

## Getting Started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Run the app

```bash
python -m src.main
```

### Running Tests

```bash
python -m pytest
```

Tests in `tests/test_recommender.py` check the `Recommender` class, CSV loading (numbers become floats/ints), that `score_song` returns a score plus reasons, that energy rewards *closeness*, and that results come back sorted highest first.

---

## Sample Recommendation Output

Output from `python -m src.main` (all profiles and the experiment):

```
Loaded songs: 18

========================================================================
Profile: Happy Pop (default)
Prefs:   genre=pop, mood=happy, energy=0.8, likes_acoustic=False
------------------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 4.39
   Because: mood match (+2.0); genre match (+1.0); energy 0.82 vs target 0.80 (+0.98); acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 3.29
   Because: mood match (+2.0); energy 0.76 vs target 0.80 (+0.96); acoustic fit (+0.33)
3. Gym Hero by Max Pulse  [pop, intense]
   Score: 2.35
   Because: genre match (+1.0); energy 0.93 vs target 0.80 (+0.87); acoustic fit (+0.47)
4. Concrete Crown by Verse Theory  [hip-hop, confident]
   Score: 1.42
   Because: energy 0.78 vs target 0.80 (+0.98); acoustic fit (+0.44)
5. Storm Runner by Voltline  [rock, intense]
   Score: 1.34
   Because: energy 0.91 vs target 0.80 (+0.89); acoustic fit (+0.45)

========================================================================
Profile: Chill Lofi
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
------------------------------------------------------------------------
1. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 4.43
   Because: mood match (+2.0); genre match (+1.0); energy 0.35 vs target 0.35 (+1.00); acoustic fit (+0.43)
2. Midnight Coding by LoRoom  [lofi, chill]
   Score: 4.29
   Because: mood match (+2.0); genre match (+1.0); energy 0.42 vs target 0.35 (+0.93); acoustic fit (+0.35)
3. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 3.39
   Because: mood match (+2.0); energy 0.28 vs target 0.35 (+0.93); acoustic fit (+0.46)
4. Focus Flow by LoRoom  [lofi, focused]
   Score: 2.34
   Because: genre match (+1.0); energy 0.40 vs target 0.35 (+0.95); acoustic fit (+0.39)
5. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 1.43
   Because: energy 0.37 vs target 0.35 (+0.98); acoustic fit (+0.45)

========================================================================
Profile: Deep Intense Rock
Prefs:   genre=rock, mood=intense, energy=0.9, likes_acoustic=False
------------------------------------------------------------------------
1. Storm Runner by Voltline  [rock, intense]
   Score: 4.44
   Because: mood match (+2.0); genre match (+1.0); energy 0.91 vs target 0.90 (+0.99); acoustic fit (+0.45)
2. Gym Hero by Max Pulse  [pop, intense]
   Score: 3.44
   Because: mood match (+2.0); energy 0.93 vs target 0.90 (+0.97); acoustic fit (+0.47)
3. Strobe Season by Kilo Drift  [edm, euphoric]
   Score: 1.44
   Because: energy 0.95 vs target 0.90 (+0.95); acoustic fit (+0.49)
4. Iron Tide by Black Harbor  [metal, angry]
   Score: 1.42
   Because: energy 0.97 vs target 0.90 (+0.93); acoustic fit (+0.48)
5. Sunrise City by Neon Echo  [pop, happy]
   Score: 1.33
   Because: energy 0.82 vs target 0.90 (+0.92); acoustic fit (+0.41)

========================================================================
Profile: Edge: High-Energy but Sad
Prefs:   genre=indie, mood=sad, energy=0.9, likes_acoustic=False
------------------------------------------------------------------------
1. Empty Platform by Grey Static  [indie, sad]
   Score: 3.56
   Because: mood match (+2.0); genre match (+1.0); energy 0.30 vs target 0.90 (+0.40); acoustic fit (+0.16)
2. Storm Runner by Voltline  [rock, intense]
   Score: 1.44
   Because: energy 0.91 vs target 0.90 (+0.99); acoustic fit (+0.45)
3. Gym Hero by Max Pulse  [pop, intense]
   Score: 1.44
   Because: energy 0.93 vs target 0.90 (+0.97); acoustic fit (+0.47)
4. Strobe Season by Kilo Drift  [edm, euphoric]
   Score: 1.44
   Because: energy 0.95 vs target 0.90 (+0.95); acoustic fit (+0.49)
5. Iron Tide by Black Harbor  [metal, angry]
   Score: 1.42
   Because: energy 0.97 vs target 0.90 (+0.93); acoustic fit (+0.48)

========================================================================
Profile: Edge: Genre Not in Catalog
Prefs:   genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
------------------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 3.29
   Because: mood match (+2.0); energy 0.82 vs target 0.70 (+0.88); acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 3.27
   Because: mood match (+2.0); energy 0.76 vs target 0.70 (+0.94); acoustic fit (+0.33)
3. Concrete Crown by Verse Theory  [hip-hop, confident]
   Score: 1.36
   Because: energy 0.78 vs target 0.70 (+0.92); acoustic fit (+0.44)
4. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 1.34
   Because: energy 0.75 vs target 0.70 (+0.95); acoustic fit (+0.39)
5. Storm Runner by Voltline  [rock, intense]
   Score: 1.24
   Because: energy 0.91 vs target 0.70 (+0.79); acoustic fit (+0.45)

########################################################################
EXPERIMENT: energy weight doubled (2.0), genre weight halved (0.5)
########################################################################
========================================================================
Profile: Happy Pop (experiment weights)
Prefs:   genre=pop, mood=happy, energy=0.8, likes_acoustic=False
------------------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 4.87
   Because: mood match (+2.0); genre match (+0.5); energy 0.82 vs target 0.80 (+1.96); acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 4.25
   Because: mood match (+2.0); energy 0.76 vs target 0.80 (+1.92); acoustic fit (+0.33)
3. Gym Hero by Max Pulse  [pop, intense]
   Score: 2.72
   Because: genre match (+0.5); energy 0.93 vs target 0.80 (+1.74); acoustic fit (+0.47)
4. Concrete Crown by Verse Theory  [hip-hop, confident]
   Score: 2.40
   Because: energy 0.78 vs target 0.80 (+1.96); acoustic fit (+0.44)
5. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 2.29
   Because: energy 0.75 vs target 0.80 (+1.90); acoustic fit (+0.39)

########################################################################
CHALLENGE 3: diversity penalty (-1.0 repeat artist, -0.5 repeat genre)
########################################################################
========================================================================
Profile: Chill Lofi (diverse)
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
------------------------------------------------------------------------
1. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 4.43
   Because: mood match (+2.0); genre match (+1.0); energy 0.35 vs target 0.35 (+1.00); acoustic fit (+0.43)
2. Midnight Coding by LoRoom  [lofi, chill]
   Score: 3.79
   Because: mood match (+2.0); genre match (+1.0); energy 0.42 vs target 0.35 (+0.93); acoustic fit (+0.35); genre already in list (-0.5)
3. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 3.39
   Because: mood match (+2.0); energy 0.28 vs target 0.35 (+0.93); acoustic fit (+0.46)
4. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 1.43
   Because: energy 0.37 vs target 0.35 (+0.98); acoustic fit (+0.45)
5. Moonlit Sonata Redux by Clara Vale  [classical, peaceful]
   Score: 1.31
   Because: energy 0.18 vs target 0.35 (+0.83); acoustic fit (+0.48)
```

---

## Experiments You Tried

**Weight shift:** I doubled the energy weight (1.0 → 2.0) and halved the genre weight (1.0 → 0.5) for the Happy Pop profile.

- The **top 3 didn't change** (Sunrise City, Rooftop Lights, Gym Hero), because mood (+2.0) still decides who is on top.
- The **bottom of the list changed**: Storm Runner (rock) dropped out and Night Drive Loop (synthwave) came in, because once energy counts double, any song around 0.8 energy can climb, whatever its genre.
- So the change made the list **different, not more accurate**. The filler songs were still songs a happy-pop fan didn't ask for.

**Edge-case profiles:** see `model_card.md`. A "high-energy but sad" user and a user whose favorite genre isn't in the catalog both exposed weaknesses.

---

## Diversity Penalty (Optional Challenge 3)

`recommend_diverse()` in `src/recommender.py` builds the top 5 one song at a time. Before each pick, any song whose **artist** is already in the list loses **1.0** point and any song whose **genre** is already in the list loses **0.5**. The penalty shows up in the reasons, e.g. `genre already in list (-0.5)`.

Effect on the Chill Lofi profile:

| Rank | Normal | With diversity penalty |
|---|---|---|
| 1 | Library Rain (lofi) | Library Rain (lofi) |
| 2 | Midnight Coding (lofi, LoRoom) | Midnight Coding (lofi, LoRoom) |
| 3 | Spacewalk Thoughts (ambient) | Spacewalk Thoughts (ambient) |
| 4 | **Focus Flow (lofi, LoRoom)** | Coffee Shop Stories (jazz) |
| 5 | Coffee Shop Stories (jazz) | **Moonlit Sonata Redux (classical)** |

Focus Flow drops out because it repeats both an artist (LoRoom) and a genre (lofi) that are already in the list, so a classical song gets a spot instead. The full output is in Sample Recommendation Output above.

---

## Limitations and Risks

- Tiny catalog: 18 songs, and most moods have only one or two songs.
- Exact string matching: "indie pop" ≠ "pop", and "k-pop" matches nothing.
- Mood is worth so much that it can override what the user said about energy.
- It doesn't understand lyrics, language, or listening history.
- The default ranking never adds variety on purpose, so the same high-energy songs (like *Gym Hero*) show up for very different users. The optional diversity penalty helps inside one list, but not across different users.

More detail is in the model card.

---

## Reflection

Read the full model card: [**Model Card**](model_card.md)

Building this showed me that a recommender is really just a scoring system. Every song gets points for how close it is to what the user said they want, then the list gets sorted. When the user's taste is simple, like my Chill Lofi profile, the results look like a real playlist. When the taste is mixed, like sad but high energy, the system just goes with whatever is worth the most points, even if that means giving a quiet song to someone who asked for loud.

Bias can show up in small choices. Making mood worth 2 points meant mood could beat everything else the user asked for. Exact text matching meant "indie pop" got no credit from a pop fan, and a k-pop fan's genre got ignored without any warning. A small catalog also made the same high energy songs fill the leftover spots for very different users. In a real app those choices would decide which artists get heard, which is a lot of power for a few numbers.
