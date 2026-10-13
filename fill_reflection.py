import re

model_reflection = """**Biggest learning moment:** The "high energy but sad" test. I set energy to 0.9 and mood to sad, expecting something loud and sad. Instead #1 was Empty Platform, a quiet 0.30 energy song. It got 3 points just for matching mood and genre, so the energy part barely mattered. That's when I got that the system doesn't understand what I want. It just adds up points, and whatever rule is worth the most wins.

**How I used AI:** I used Claude for most of this project. It wrote the code in recommender.py and main.py, the tests, and the first drafts of the README and this model card. I made the design calls, like making mood worth 2 points and genre 1 point because the feeling of a song matters more to me than the genre label. I also ran everything on my own laptop and checked that the results made sense before I committed. Where I had to slow down was the explanations. I didn't want to just trust that the rankings were right, so I went through the reasons in the output, like "mood match (+2.0)", to see why each song landed where it did.

**What surprised me:** How real the Chill Lofi list looks. Library Rain, Midnight Coding, Spacewalk Thoughts, Focus Flow and Coffee Shop Stories honestly sound like a playlist I'd put on to study, and it came from a few points being added together. But one weird combo like sad and high energy and it falls apart, so it only "feels" smart when your taste is simple.

**What I'd try next:** Stop the same songs from showing up for everyone. Gym Hero and Storm Runner kept popping up in the top 5 for totally different people. I'd add a penalty so once a genre or artist is already in the list, the next song from it scores lower and something different gets a chance."""

readme_reflection = """Building this showed me that a recommender is really just a scoring system. Every song gets points for how close it is to what the user said they want, then the list gets sorted. When the user's taste is simple, like my Chill Lofi profile, the results look like a real playlist. When the taste is mixed, like sad but high energy, the system just goes with whatever is worth the most points, even if that means giving a quiet song to someone who asked for loud.

Bias can show up in small choices. Making mood worth 2 points meant mood could beat everything else the user asked for. Exact text matching meant "indie pop" got no credit from a pop fan, and a k-pop fan's genre got ignored without any warning. A small catalog also made the same high energy songs fill the leftover spots for very different users. In a real app those choices would decide which artists get heard, which is a lot of power for a few numbers."""

m = open("model_card.md").read()
m2 = re.sub(r"(## 9\. Personal Reflection\s*\n\n)<!--.*?-->", lambda x: x.group(1) + model_reflection, m, flags=re.S)
assert m2 != m, "model_card.md reflection comment not found - paste section 9 to Claude"
open("model_card.md", "w").write(m2)
print("✅ model_card.md: personal reflection added")

r = open("README.md").read()
r2 = re.sub(r"<!-- Write 1.2 paragraphs IN YOUR OWN WORDS.*?-->", lambda x: readme_reflection, r, flags=re.S)
assert r2 != r, "README reflection comment not found - paste the Reflection section to Claude"
open("README.md", "w").write(r2)
print("✅ README.md: reflection added")
