# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch 1.0**

---

## 2. Intended Use

MoodMatch suggests 5 songs from a small catalog based on a listener's favorite mood, favorite genre, target energy level, and whether they like acoustic music. It assumes the user can describe their taste with one mood and one genre, and that what they want right now is mostly about *feeling*.

**Intended use:** classroom exploration of how recommendation systems turn data into suggestions, and where they go wrong.

**Not intended for:** real users or a real music app. It knows nothing about listening history, lyrics, language, or culture, and its 18-song catalog is far too small to represent anyone's actual taste. It also shouldn't be used to judge which artists or genres are "better," because its scores only measure similarity to one profile.

---

## 3. How the Model Works

Every song gets points for how well it matches the listener:

- **Same mood as the listener:** +2 points. This is the biggest factor, because the feeling of a song matters most.
- **Same genre:** +1 point.
- **Energy:** up to +1 point. The closer the song's energy is to what the listener wants, the more points it gets. A perfect match gets the full point; a song that's way too calm or way too intense gets very few.
- **Acoustic fit:** up to +0.5. Acoustic songs earn more for listeners who like acoustic music; electronic songs earn more for listeners who don't.

Then every song in the catalog is sorted by points, and the top 5 are shown along with the reasons each one earned its score.

**Changes from the starter logic:** the starter `recommend` just returned the first 5 songs in the file. I made mood worth more than genre (the common starting recipe does the opposite), and added an acoustic-fit bonus using the `likes_acoustic` field.

---

## 4. Data

- **18 songs.** The original 10, plus 8 I added to cover genres and moods that were missing.
- **Genres (15):** pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip-hop, classical, metal, r&b, country, edm, reggae, indie.
- **Moods (13):** happy, chill, intense, relaxed, moody, focused, confident, peaceful, angry, romantic, nostalgic, euphoric, sad.
- **Features:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness, plus 5 I added later: popularity, release_decade, mood_tags, instrumentalness, speechiness. Genre, mood, energy, and acousticness are always scored. The 5 new ones only count when a user asks for them.
- **Gaps:** most moods have only 1–2 songs. Lofi has 3 songs, more than any other genre. There are no lyrics or languages, and the songs are mostly Western genres. The popularity numbers and mood tags are made up for this simulation, not real data.

---

## 5. Strengths

- **Clear, single-genre tastes work well.** Chill Lofi got Library Rain and Midnight Coding at the top, and Deep Intense Rock got Storm Runner. Those match my intuition.
- **Energy rewards closeness, not "more."** A listener who wants 0.35 energy gets songs near 0.35, not the calmest song in the catalog.
- **Every recommendation explains itself**, e.g. `mood match (+2.0); genre match (+1.0); energy 0.82 vs target 0.80 (+0.98)`, so you can see exactly why a song ranked where it did.
- **Mood can cross genres.** Spacewalk Thoughts (ambient) still ranked #3 for the chill lofi listener because the mood matched.

---

## 6. Limitations and Bias

The biggest weakness I found is that **mood can override everything else the user asked for.** For the "High-Energy but Sad" profile (indie, sad, energy 0.9), the #1 song was *Empty Platform*, a quiet 0.30-energy track. It earned 3.0 points just for matching mood and genre, while its energy was a terrible match. Meanwhile the high-energy songs that actually fit "0.9" all tied around 1.44 and had nothing to do with sadness. The system can't represent a mixed request like "sad but loud." It simply follows whichever rule is worth the most points. A second bias is **exact text matching**: *Rooftop Lights* is "indie pop," so it never gets genre credit from a "pop" fan, and a "k-pop" fan's genre is silently ignored. A third is the **filter bubble effect of a small catalog**: high-energy songs like *Gym Hero* and *Storm Runner* show up in the top 5 for Happy Pop, Deep Intense Rock, and the sad edge case alike, because once the one or two mood matches are used up, the remaining spots go to whatever has a similar energy.

---

## 7. Evaluation

**Profiles tested:** Happy Pop (the default), Chill Lofi, Deep Intense Rock, plus two edge cases: "High-Energy but Sad" (conflicting preferences) and "Genre Not in Catalog" (k-pop). I also ran one experiment: double the energy weight, halve the genre weight.

**What I looked for:** whether #1 matched what I'd pick myself, whether the reasons made sense, and which songs kept reappearing.

**Comparisons between profiles:**

- **Happy Pop vs. Chill Lofi:** the lists share **no songs at all**. Happy Pop pulls bright, ~0.8-energy songs (Sunrise City, Rooftop Lights), while Chill Lofi shifts to calm, acoustic tracks around 0.35 energy (Library Rain, Midnight Coding). That makes sense, because the two profiles disagree on mood, genre, energy, *and* acoustic preference.
- **Happy Pop vs. Deep Intense Rock:** both lists contain *Gym Hero*, but for different reasons. For Happy Pop it ranks #3 only because it is tagged "pop" and is high energy, even though its mood is *intense*, not happy. For the Rock profile it ranks #2 because its mood (intense) matches. In plain language: Gym Hero keeps showing up for people who just want happy pop because the system sees "pop + lots of energy" and doesn't realize a workout anthem isn't a happy song.
- **Chill Lofi vs. Deep Intense Rock:** completely opposite ends of the energy scale (0.35 vs. 0.9), and the results flip accordingly: acoustic, slow songs for one, electronic and loud for the other. This shows the energy and acoustic rules are actually doing their job.
- **Deep Intense Rock vs. High-Energy but Sad:** both want ~0.9 energy, so the same loud songs (Storm Runner, Gym Hero, Strobe Season, Iron Tide) fill spots 2–5 for both. The difference is #1: Rock gets a true match, while the sad profile gets a *quiet* sad song because mood outweighs energy.
- **Happy Pop vs. Genre Not in Catalog (k-pop, happy):** nearly the same list. The k-pop genre is ignored, so the system quietly falls back to mood and energy and serves regular pop, without telling the user their genre wasn't found.

**Experiment results (energy ×2, genre ×0.5, Happy Pop):** the top 3 stayed the same, but Storm Runner was replaced by Night Drive Loop in the top 5. The change made the list **different, not more accurate**: the filler songs still weren't happy pop.

**What surprised me:** how much a simple point system *feels* like a real recommendation when it works (the chill lofi list looks like a real study playlist), and how quickly it falls apart for anyone whose taste doesn't fit one mood and one genre.

---

## 8. Future Work

1. **Partial genre matching:** give "indie pop" partial credit for a "pop" fan (for example, half the genre points when one genre name contains the other).
2. **Variety across users, not just inside one list:** I added a diversity penalty that stops one top 5 from repeating an artist or genre, but Gym Hero can still show up for very different users. Next I'd track which songs get recommended most and lower their scores a little.
3. **Multiple moods per user:** let a listener say "sad *and* energetic," and use valence (how positive a song sounds) to tell sad songs from happy ones instead of relying on one mood tag.

---

## 9. Personal Reflection

**Biggest learning moment:** The "high energy but sad" test. I set energy to 0.9 and mood to sad, expecting something loud and sad. Instead #1 was Empty Platform, a quiet 0.30 energy song. It got 3 points just for matching mood and genre, so the energy part barely mattered. That's when I got that the system doesn't understand what I want. It just adds up points, and whatever rule is worth the most wins.

**How I used AI:** I used Claude for most of this project. It wrote the code in recommender.py and main.py, the tests, and the first drafts of the README and this model card. I made the design calls, like making mood worth 2 points and genre 1 point because the feeling of a song matters more to me than the genre label. I also ran everything on my own laptop and checked that the results made sense before I committed. Where I had to slow down was the explanations. I didn't want to just trust that the rankings were right, so I went through the reasons in the output, like "mood match (+2.0)", to see why each song landed where it did.

**What surprised me:** How real the Chill Lofi list looks. Library Rain, Midnight Coding, Spacewalk Thoughts, Focus Flow and Coffee Shop Stories honestly sound like a playlist I'd put on to study, and it came from a few points being added together. But one weird combo like sad and high energy and it falls apart, so it only "feels" smart when your taste is simple.

**What I'd try next:** Stop the same songs from showing up for everyone. Gym Hero and Storm Runner kept popping up in the top 5 for totally different people. I'd add a penalty so once a genre or artist is already in the list, the next song from it scores lower and something different gets a chance.
