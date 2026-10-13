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

User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False
Top recommendations:

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
```

---

## Reflection

Read the full model card: [**Model Card**](model_card.md)

<!-- Write 1–2 paragraphs IN YOUR OWN WORDS. Questions to answer:
  - What did you learn about how recommenders turn data into predictions?
  - Where could bias or unfairness show up in systems like this?
  Delete this comment when you're done. -->
