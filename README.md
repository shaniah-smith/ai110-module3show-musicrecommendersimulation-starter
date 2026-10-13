# 🎵 Music Recommender Simulation

## Project Summary

This project is a small **content-based music recommender** written in Python. It reads a catalog of 18 songs from `data/songs.csv`, compares each song to a user's "taste profile" (favorite mood, favorite genre, target energy, and whether they like acoustic music), gives every song a score with a list of reasons, and returns the top 5. The goal is to understand, and explain, how apps like Spotify turn data into "you might like this," and where that process can go wrong.

---

## How The System Works

### How real recommenders work

Real platforms like Spotify and YouTube mostly combine two ideas. **Collaborative filtering** looks at other people's behavior: if listeners who like the same songs as you also play song X, you'll probably like song X too. It uses likes, skips, replays, playlist adds, and listening time. **Content-based filtering** looks at the songs themselves (genre, mood, tempo, energy, acousticness) and finds songs that are similar to what you already like. Collaborative filtering is great at surprising discoveries but can't recommend a brand-new song nobody has played yet. Content-based filtering works for any song but tends to keep giving you more of the same.

**My version is content-based only**, because there are no other users in this simulation, just song attributes. It prioritizes **mood first**, because to me the feeling of a song matters more than the label on it. Then it looks at genre, then how close the energy is.

### Features used

**`Song`:** `genre`, `mood`, `energy` (0–1), and `acousticness` (0–1) are used in scoring. `title`, `artist`, `tempo_bpm`, `valence`, and `danceability` are stored but not scored. The optional advanced features (`popularity`, `release_decade`, `mood_tags`, `instrumentalness`, `speechiness`) only score when a user asks for them (see Optional Challenges below).

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
python -m src.main                        # default: Mood-First mode
python -m src.main --mode genre_first     # Genre-First mode
python -m src.main --mode energy_focused  # Energy-Focused mode
```

### Running Tests

```bash
python -m pytest
```

Tests in `tests/test_recommender.py` check the `Recommender` class, CSV loading (numbers become floats/ints), that `score_song` returns a score plus reasons, that energy rewards *closeness*, that results come back sorted highest first, the diversity penalty, the new song features, and that the scoring modes actually change the ranking (11 tests).

---

## Sample Recommendation Output

Output from `python -m src.main` (all profiles and the experiment):

```
Loaded songs: 18
Scoring mode: Mood-First (Feeling matters most (the default recipe))

==============================================================================
Profile: Happy Pop (default)
Prefs:   genre=pop, mood=happy, energy=0.8, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Sunrise City    | pop            |    4.39 | mood match (+2.0)                  |
|     | Neon Echo       | happy          |         | genre match (+1.0)                 |
|     |                 |                |         | energy 0.82 vs target 0.80 (+0.98) |
|     |                 |                |         | acoustic fit (+0.41)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Rooftop Lights  | indie pop      |    3.29 | mood match (+2.0)                  |
|     | Indigo Parade   | happy          |         | energy 0.76 vs target 0.80 (+0.96) |
|     |                 |                |         | acoustic fit (+0.33)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Gym Hero        | pop            |    2.35 | genre match (+1.0)                 |
|     | Max Pulse       | intense        |         | energy 0.93 vs target 0.80 (+0.87) |
|     |                 |                |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Concrete Crown  | hip-hop        |    1.42 | energy 0.78 vs target 0.80 (+0.98) |
|     | Verse Theory    | confident      |         | acoustic fit (+0.44)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Storm Runner    | rock           |    1.34 | energy 0.91 vs target 0.80 (+0.89) |
|     | Voltline        | intense        |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Chill Lofi
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
+-----+---------------------+----------------+---------+------------------------------------+
|   # | Song / Artist       | Genre / Mood   |   Score | Why it was picked                  |
+=====+=====================+================+=========+====================================+
|   1 | Library Rain        | lofi           |    4.43 | mood match (+2.0)                  |
|     | Paper Lanterns      | chill          |         | genre match (+1.0)                 |
|     |                     |                |         | energy 0.35 vs target 0.35 (+1.00) |
|     |                     |                |         | acoustic fit (+0.43)               |
+-----+---------------------+----------------+---------+------------------------------------+
|   2 | Midnight Coding     | lofi           |    4.29 | mood match (+2.0)                  |
|     | LoRoom              | chill          |         | genre match (+1.0)                 |
|     |                     |                |         | energy 0.42 vs target 0.35 (+0.93) |
|     |                     |                |         | acoustic fit (+0.35)               |
+-----+---------------------+----------------+---------+------------------------------------+
|   3 | Spacewalk Thoughts  | ambient        |    3.39 | mood match (+2.0)                  |
|     | Orbit Bloom         | chill          |         | energy 0.28 vs target 0.35 (+0.93) |
|     |                     |                |         | acoustic fit (+0.46)               |
+-----+---------------------+----------------+---------+------------------------------------+
|   4 | Focus Flow          | lofi           |    2.34 | genre match (+1.0)                 |
|     | LoRoom              | focused        |         | energy 0.40 vs target 0.35 (+0.95) |
|     |                     |                |         | acoustic fit (+0.39)               |
+-----+---------------------+----------------+---------+------------------------------------+
|   5 | Coffee Shop Stories | jazz           |    1.43 | energy 0.37 vs target 0.35 (+0.98) |
|     | Slow Stereo         | relaxed        |         | acoustic fit (+0.45)               |
+-----+---------------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Deep Intense Rock
Prefs:   genre=rock, mood=intense, energy=0.9, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Storm Runner    | rock           |    4.44 | mood match (+2.0)                  |
|     | Voltline        | intense        |         | genre match (+1.0)                 |
|     |                 |                |         | energy 0.91 vs target 0.90 (+0.99) |
|     |                 |                |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Gym Hero        | pop            |    3.44 | mood match (+2.0)                  |
|     | Max Pulse       | intense        |         | energy 0.93 vs target 0.90 (+0.97) |
|     |                 |                |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Strobe Season   | edm            |    1.44 | energy 0.95 vs target 0.90 (+0.95) |
|     | Kilo Drift      | euphoric       |         | acoustic fit (+0.49)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Iron Tide       | metal          |    1.42 | energy 0.97 vs target 0.90 (+0.93) |
|     | Black Harbor    | angry          |         | acoustic fit (+0.48)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Sunrise City    | pop            |    1.33 | energy 0.82 vs target 0.90 (+0.92) |
|     | Neon Echo       | happy          |         | acoustic fit (+0.41)               |
+-----+-----------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Edge: High-Energy but Sad
Prefs:   genre=indie, mood=sad, energy=0.9, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Empty Platform  | indie          |    3.56 | mood match (+2.0)                  |
|     | Grey Static     | sad            |         | genre match (+1.0)                 |
|     |                 |                |         | energy 0.30 vs target 0.90 (+0.40) |
|     |                 |                |         | acoustic fit (+0.16)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Storm Runner    | rock           |    1.44 | energy 0.91 vs target 0.90 (+0.99) |
|     | Voltline        | intense        |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Gym Hero        | pop            |    1.44 | energy 0.93 vs target 0.90 (+0.97) |
|     | Max Pulse       | intense        |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Strobe Season   | edm            |    1.44 | energy 0.95 vs target 0.90 (+0.95) |
|     | Kilo Drift      | euphoric       |         | acoustic fit (+0.49)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Iron Tide       | metal          |    1.42 | energy 0.97 vs target 0.90 (+0.93) |
|     | Black Harbor    | angry          |         | acoustic fit (+0.48)               |
+-----+-----------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Edge: Genre Not in Catalog
Prefs:   genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
+-----+------------------+----------------+---------+------------------------------------+
|   # | Song / Artist    | Genre / Mood   |   Score | Why it was picked                  |
+=====+==================+================+=========+====================================+
|   1 | Sunrise City     | pop            |    3.29 | mood match (+2.0)                  |
|     | Neon Echo        | happy          |         | energy 0.82 vs target 0.70 (+0.88) |
|     |                  |                |         | acoustic fit (+0.41)               |
+-----+------------------+----------------+---------+------------------------------------+
|   2 | Rooftop Lights   | indie pop      |    3.27 | mood match (+2.0)                  |
|     | Indigo Parade    | happy          |         | energy 0.76 vs target 0.70 (+0.94) |
|     |                  |                |         | acoustic fit (+0.33)               |
+-----+------------------+----------------+---------+------------------------------------+
|   3 | Concrete Crown   | hip-hop        |    1.36 | energy 0.78 vs target 0.70 (+0.92) |
|     | Verse Theory     | confident      |         | acoustic fit (+0.44)               |
+-----+------------------+----------------+---------+------------------------------------+
|   4 | Night Drive Loop | synthwave      |    1.34 | energy 0.75 vs target 0.70 (+0.95) |
|     | Neon Echo        | moody          |         | acoustic fit (+0.39)               |
+-----+------------------+----------------+---------+------------------------------------+
|   5 | Storm Runner     | rock           |    1.24 | energy 0.91 vs target 0.70 (+0.79) |
|     | Voltline         | intense        |         | acoustic fit (+0.45)               |
+-----+------------------+----------------+---------+------------------------------------+

##############################################################################
EXPERIMENT: energy weight doubled (2.0), genre weight halved (0.5)
##############################################################################
==============================================================================
Profile: Happy Pop (experiment weights)
Prefs:   genre=pop, mood=happy, energy=0.8, likes_acoustic=False
+-----+------------------+----------------+---------+------------------------------------+
|   # | Song / Artist    | Genre / Mood   |   Score | Why it was picked                  |
+=====+==================+================+=========+====================================+
|   1 | Sunrise City     | pop            |    4.87 | mood match (+2.0)                  |
|     | Neon Echo        | happy          |         | genre match (+0.5)                 |
|     |                  |                |         | energy 0.82 vs target 0.80 (+1.96) |
|     |                  |                |         | acoustic fit (+0.41)               |
+-----+------------------+----------------+---------+------------------------------------+
|   2 | Rooftop Lights   | indie pop      |    4.25 | mood match (+2.0)                  |
|     | Indigo Parade    | happy          |         | energy 0.76 vs target 0.80 (+1.92) |
|     |                  |                |         | acoustic fit (+0.33)               |
+-----+------------------+----------------+---------+------------------------------------+
|   3 | Gym Hero         | pop            |    2.72 | genre match (+0.5)                 |
|     | Max Pulse        | intense        |         | energy 0.93 vs target 0.80 (+1.74) |
|     |                  |                |         | acoustic fit (+0.47)               |
+-----+------------------+----------------+---------+------------------------------------+
|   4 | Concrete Crown   | hip-hop        |    2.4  | energy 0.78 vs target 0.80 (+1.96) |
|     | Verse Theory     | confident      |         | acoustic fit (+0.44)               |
+-----+------------------+----------------+---------+------------------------------------+
|   5 | Night Drive Loop | synthwave      |    2.29 | energy 0.75 vs target 0.80 (+1.90) |
|     | Neon Echo        | moody          |         | acoustic fit (+0.39)               |
+-----+------------------+----------------+---------+------------------------------------+

##############################################################################
CHALLENGE 1: advanced features (decade, mood tags, popularity, focus mode)
##############################################################################
==============================================================================
Profile: Late-Night Underground Jazz
Prefs:   genre=jazz, mood=relaxed, energy=0.4, likes_acoustic=True, preferred_decade=2010s, mood_tags=['cozy', 'late-night'], popularity_pref=underground, focus_mode=True
+-----+---------------------+----------------+---------+----------------------------------------+
|   # | Song / Artist       | Genre / Mood   |   Score | Why it was picked                      |
+=====+=====================+================+=========+========================================+
|   1 | Coffee Shop Stories | jazz           |    5.37 | mood match (+2.0)                      |
|     | Slow Stereo         | relaxed        |         | genre match (+1.0)                     |
|     |                     |                |         | energy 0.37 vs target 0.40 (+0.97)     |
|     |                     |                |         | acoustic fit (+0.45)                   |
|     |                     |                |         | mood tags cozy (+0.25)                 |
|     |                     |                |         | underground fit, popularity 42 (+0.29) |
|     |                     |                |         | focus fit (+0.41)                      |
+-----+---------------------+----------------+---------+----------------------------------------+
|   2 | Island Slowburn     | reggae         |    3.71 | mood match (+2.0)                      |
|     | Roots Avenue        | relaxed        |         | energy 0.50 vs target 0.40 (+0.90)     |
|     |                     |                |         | acoustic fit (+0.28)                   |
|     |                     |                |         | underground fit, popularity 46 (+0.27) |
|     |                     |                |         | focus fit (+0.26)                      |
+-----+---------------------+----------------+---------+----------------------------------------+
|   3 | Spacewalk Thoughts  | ambient        |    2.65 | energy 0.28 vs target 0.40 (+0.88)     |
|     | Orbit Bloom         | chill          |         | acoustic fit (+0.46)                   |
|     |                     |                |         | from the 2010s (+0.50)                 |
|     |                     |                |         | underground fit, popularity 34 (+0.33) |
|     |                     |                |         | focus fit (+0.48)                      |
+-----+---------------------+----------------+---------+----------------------------------------+
|   4 | Midnight Coding     | lofi           |    2.52 | energy 0.42 vs target 0.40 (+0.98)     |
|     | LoRoom              | chill          |         | acoustic fit (+0.35)                   |
|     |                     |                |         | mood tags cozy, late-night (+0.50)     |
|     |                     |                |         | underground fit, popularity 55 (+0.22) |
|     |                     |                |         | focus fit (+0.46)                      |
+-----+---------------------+----------------+---------+----------------------------------------+
|   5 | Empty Platform      | indie          |    2.37 | energy 0.30 vs target 0.40 (+0.90)     |
|     | Grey Static         | sad            |         | acoustic fit (+0.34)                   |
|     |                     |                |         | from the 2010s (+0.50)                 |
|     |                     |                |         | underground fit, popularity 37 (+0.32) |
|     |                     |                |         | focus fit (+0.32)                      |
+-----+---------------------+----------------+---------+----------------------------------------+

##############################################################################
CHALLENGE 2: same profile, three scoring modes
##############################################################################
==============================================================================
Profile: Edge: High-Energy but Sad / Mood-First
Prefs:   genre=indie, mood=sad, energy=0.9, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Empty Platform  | indie          |    3.56 | mood match (+2.0)                  |
|     | Grey Static     | sad            |         | genre match (+1.0)                 |
|     |                 |                |         | energy 0.30 vs target 0.90 (+0.40) |
|     |                 |                |         | acoustic fit (+0.16)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Storm Runner    | rock           |    1.44 | energy 0.91 vs target 0.90 (+0.99) |
|     | Voltline        | intense        |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Gym Hero        | pop            |    1.44 | energy 0.93 vs target 0.90 (+0.97) |
|     | Max Pulse       | intense        |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Strobe Season   | edm            |    1.44 | energy 0.95 vs target 0.90 (+0.95) |
|     | Kilo Drift      | euphoric       |         | acoustic fit (+0.49)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Iron Tide       | metal          |    1.42 | energy 0.97 vs target 0.90 (+0.93) |
|     | Black Harbor    | angry          |         | acoustic fit (+0.48)               |
+-----+-----------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Edge: High-Energy but Sad / Genre-First
Prefs:   genre=indie, mood=sad, energy=0.9, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Empty Platform  | indie          |    3.56 | mood match (+1.0)                  |
|     | Grey Static     | sad            |         | genre match (+2.0)                 |
|     |                 |                |         | energy 0.30 vs target 0.90 (+0.40) |
|     |                 |                |         | acoustic fit (+0.16)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Storm Runner    | rock           |    1.44 | energy 0.91 vs target 0.90 (+0.99) |
|     | Voltline        | intense        |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Gym Hero        | pop            |    1.44 | energy 0.93 vs target 0.90 (+0.97) |
|     | Max Pulse       | intense        |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Strobe Season   | edm            |    1.44 | energy 0.95 vs target 0.90 (+0.95) |
|     | Kilo Drift      | euphoric       |         | acoustic fit (+0.49)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Iron Tide       | metal          |    1.42 | energy 0.97 vs target 0.90 (+0.93) |
|     | Black Harbor    | angry          |         | acoustic fit (+0.48)               |
+-----+-----------------+----------------+---------+------------------------------------+

==============================================================================
Profile: Edge: High-Energy but Sad / Energy-Focused
Prefs:   genre=indie, mood=sad, energy=0.9, likes_acoustic=False
+-----+-----------------+----------------+---------+------------------------------------+
|   # | Song / Artist   | Genre / Mood   |   Score | Why it was picked                  |
+=====+=================+================+=========+====================================+
|   1 | Storm Runner    | rock           |    2.93 | energy 0.91 vs target 0.90 (+2.48) |
|     | Voltline        | intense        |         | acoustic fit (+0.45)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   2 | Gym Hero        | pop            |    2.9  | energy 0.93 vs target 0.90 (+2.42) |
|     | Max Pulse       | intense        |         | acoustic fit (+0.47)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   3 | Strobe Season   | edm            |    2.87 | energy 0.95 vs target 0.90 (+2.38) |
|     | Kilo Drift      | euphoric       |         | acoustic fit (+0.49)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   4 | Iron Tide       | metal          |    2.81 | energy 0.97 vs target 0.90 (+2.33) |
|     | Black Harbor    | angry          |         | acoustic fit (+0.48)               |
+-----+-----------------+----------------+---------+------------------------------------+
|   5 | Sunrise City    | pop            |    2.71 | energy 0.82 vs target 0.90 (+2.30) |
|     | Neon Echo       | happy          |         | acoustic fit (+0.41)               |
+-----+-----------------+----------------+---------+------------------------------------+

##############################################################################
CHALLENGE 3: diversity penalty (-1.0 repeat artist, -0.5 repeat genre)
##############################################################################
==============================================================================
Profile: Chill Lofi (diverse)
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
+-----+----------------------+----------------+---------+------------------------------------+
|   # | Song / Artist        | Genre / Mood   |   Score | Why it was picked                  |
+=====+======================+================+=========+====================================+
|   1 | Library Rain         | lofi           |    4.43 | mood match (+2.0)                  |
|     | Paper Lanterns       | chill          |         | genre match (+1.0)                 |
|     |                      |                |         | energy 0.35 vs target 0.35 (+1.00) |
|     |                      |                |         | acoustic fit (+0.43)               |
+-----+----------------------+----------------+---------+------------------------------------+
|   2 | Midnight Coding      | lofi           |    3.79 | mood match (+2.0)                  |
|     | LoRoom               | chill          |         | genre match (+1.0)                 |
|     |                      |                |         | energy 0.42 vs target 0.35 (+0.93) |
|     |                      |                |         | acoustic fit (+0.35)               |
|     |                      |                |         | genre already in list (-0.5)       |
+-----+----------------------+----------------+---------+------------------------------------+
|   3 | Spacewalk Thoughts   | ambient        |    3.39 | mood match (+2.0)                  |
|     | Orbit Bloom          | chill          |         | energy 0.28 vs target 0.35 (+0.93) |
|     |                      |                |         | acoustic fit (+0.46)               |
+-----+----------------------+----------------+---------+------------------------------------+
|   4 | Coffee Shop Stories  | jazz           |    1.43 | energy 0.37 vs target 0.35 (+0.98) |
|     | Slow Stereo          | relaxed        |         | acoustic fit (+0.45)               |
+-----+----------------------+----------------+---------+------------------------------------+
|   5 | Moonlit Sonata Redux | classical      |    1.31 | energy 0.18 vs target 0.35 (+0.83) |
|     | Clara Vale           | peaceful       |         | acoustic fit (+0.48)               |
+-----+----------------------+----------------+---------+------------------------------------+
```

---

## Experiments You Tried

**Weight shift:** I doubled the energy weight (1.0 → 2.0) and halved the genre weight (1.0 → 0.5) for the Happy Pop profile.

- The **top 3 didn't change** (Sunrise City, Rooftop Lights, Gym Hero), because mood (+2.0) still decides who is on top.
- The **bottom of the list changed**: Storm Runner (rock) dropped out and Night Drive Loop (synthwave) came in, because once energy counts double, any song around 0.8 energy can climb, whatever its genre.
- So the change made the list **different, not more accurate**. The filler songs were still songs a happy-pop fan didn't ask for.

**Edge-case profiles:** see `model_card.md`. A "high-energy but sad" user and a user whose favorite genre isn't in the catalog both exposed weaknesses.

---

## Optional Challenges

### Challenge 1: Advanced song features

I added 5 new columns to `data/songs.csv` for all 18 songs:

| Column | Example | Scored when the user sets... | Points |
|---|---|---|---|
| `popularity` (0–100) | 82 | `popularity_pref`: `"popular"` or `"underground"` | up to +0.5 |
| `release_decade` | 2010s | `preferred_decade` | +0.5 on a match |
| `mood_tags` | `cozy;nostalgic;late-night` | `mood_tags` (a list) | +0.25 per shared tag, max 2 |
| `instrumentalness` (0–1) | 0.88 | `focus_mode: True` | up to +0.5, averaged with speechiness |
| `speechiness` (0–1) | 0.04 | `focus_mode: True` | (low talking = more points) |

These only add points when a profile asks for them, so all the original profiles score exactly the same as before. The "Late-Night Underground Jazz" profile in the output uses all of them. Coffee Shop Stories wins with 5.37, and Spacewalk Thoughts jumps to #3 because it is from the 2010s, very instrumental, and not very popular.

### Challenge 2: Scoring modes (Strategy pattern)

Each mode is a `ScoringMode` object in `src/recommender.py` with its own weights and a `score()` method. `recommend_with_mode()` takes a mode name, so switching strategies doesn't change any other code.

| Mode | Mood | Genre | Energy | Use it when... |
|---|---|---|---|---|
| `mood_first` (default) | 2.0 | 1.0 | 1.0 | the feeling matters most |
| `genre_first` | 1.0 | 2.0 | 1.0 | you want to stay in one genre |
| `energy_focused` | 1.0 | 0.5 | 2.5 | you care about intensity more than labels |

Switch modes with `python -m src.main --mode energy_focused`. The output also compares all three modes on the "High-Energy but Sad" profile. Mood-First and Genre-First both put quiet *Empty Platform* at #1, while Energy-Focused finally gives that user loud songs (*Storm Runner*, *Gym Hero*), which fixes the problem from my reflection.

### Challenge 4: Visual summary table

`print_table()` in `src/main.py` uses the `tabulate` library (`tablefmt="grid"`) to show each result as a table row with rank, song and artist, genre and mood, score, and a **"Why it was picked"** column that lists every reason on its own line. If `tabulate` isn't installed, it falls back to plain text so the program still runs. `tabulate` was added to `requirements.txt`.

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
