# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

### Challenge 3: Diversity penalty

**What task did you give the agent?**

I asked Claude to build Optional Challenge 3, a diversity penalty, because in my testing the same songs kept showing up and the Chill Lofi list had two LoRoom songs in it. I wanted the recommender to stop stacking the same artist or genre in the top 5.

**Prompts used:**

Roughly: "Build the diversity penalty challenge for my music recommender and give me terminal commands." Before that I had told it the change I'd want next was to stop repeat songs from showing up for everyone.

**What did the agent generate or change?**

- `src/recommender.py`: added `recommend_diverse()` and `DIVERSITY_PENALTY` (-1.0 for a repeat artist, -0.5 for a repeat genre). It picks songs one at a time and re-checks the penalty after every pick.
- `src/main.py`: added a "Chill Lofi (diverse)" run at the end of the output.
- `tests/test_recommender.py`: added a test that Focus Flow is in the normal lofi list but gets pushed out of the diverse one.
- `README.md`: added a Diversity Penalty section with a before/after table.

**What did you verify or fix manually?**

I ran `python -m src.main` and `python -m pytest` on my laptop and compared the normal and diverse Chill Lofi lists. Focus Flow (LoRoom, lofi) dropped out and Moonlit Sonata Redux (classical) took its spot, which is what I wanted. I also checked that Library Rain stayed #1 with the same score, since it's the first pick and nothing should be penalized yet. Midnight Coding still made #2 even with the -0.5 genre penalty, which makes sense because it's a strong mood and genre match.


### Challenge 1: Advanced song features

**What task did you give the agent?**

After Challenge 3, I asked Claude to go back and do all the optional challenges I had skipped. For Challenge 1 that meant adding 5 new song attributes to the dataset and making the scoring use them.

**Prompts used:**

"go back and unskip do all of the extra challenges"

**What did the agent generate or change?**

- `data/songs.csv`: added `popularity`, `release_decade`, `mood_tags`, `instrumentalness`, and `speechiness` to all 18 songs. The values are made up to fit each song's vibe.
- `src/recommender.py`: `load_songs()` turns the new numbers into floats and splits `mood_tags` into a list. `score_song()` adds points for a matching decade, shared mood tags, popular vs underground, and a "focus mode" that likes instrumental songs with little talking. These only count if the user's profile asks for them.
- `src/main.py`: added a "Late-Night Underground Jazz" profile that uses every new feature.
- `tests/test_recommender.py`: tests that the new columns load correctly and only add points when the user asks.

**What did you verify or fix manually?**

I checked that my original 5 profiles still give the same scores as before, so the README tables and model card are still right. Then I looked at the new profile's results. Coffee Shop Stories won, which makes sense since it is jazz, relaxed, and cozy. Spacewalk Thoughts got bumped to #3 because of the decade, focus, and underground points, which shows the new features are really doing something.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

**Strategy pattern.** Each scoring mode (Mood-First, Genre-First, Energy-Focused) is its own `ScoringMode` object with the same `score()` method, so the recommender can swap one for another without any if/else chains.

**How did AI help you brainstorm or implement it?**

I asked Claude to do Challenge 2 along with the other optional challenges. It suggested the Strategy pattern because my three modes only differ in their weights. Each mode can be a small object that holds its weights, and the ranking code just calls `mode.score()` without caring which mode it is. That also meant the default Mood-First mode reuses my original `score_song()`, so nothing I had already tested changed. When I compared the modes on the "High-Energy but Sad" profile, Energy-Focused finally gave that user loud songs instead of quiet Empty Platform. That was the exact problem I wrote about in my reflection, so it showed me the modes actually matter.

**How does the pattern appear in your final code?**

- `ScoringMode` class in `src/recommender.py`: holds a name, a description, and weights, and has `score(user_prefs, song)`.
- `SCORING_MODES` dictionary: the three strategies (`mood_first`, `genre_first`, `energy_focused`).
- `recommend_with_mode()`: looks up the strategy by name and ranks every song with `strategy.score()`.
- `src/main.py`: `--mode` lets the user switch strategies, e.g. `python -m src.main --mode energy_focused`.
