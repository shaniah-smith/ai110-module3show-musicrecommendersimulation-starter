# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

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

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
