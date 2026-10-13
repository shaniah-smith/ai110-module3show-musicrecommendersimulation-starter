from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ---- Functional API tests -------------------------------------------------- #
from src.recommender import load_songs, score_song, recommend_songs


def test_load_songs_converts_numbers():
    songs = load_songs("data/songs.csv")
    assert len(songs) >= 10
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["id"], int)


def test_score_song_returns_score_and_reasons():
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, song)
    assert score == 4.0  # mood 2.0 + genre 1.0 + perfect energy 1.0
    assert any("mood match" in r for r in reasons)
    assert any("genre match" in r for r in reasons)


def test_energy_rewards_closeness_not_just_high_values():
    prefs = {"genre": "x", "mood": "x", "energy": 0.4}
    close, _ = score_song(prefs, {"genre": "a", "mood": "b", "energy": 0.4, "acousticness": 0.5})
    too_high, _ = score_song(prefs, {"genre": "a", "mood": "b", "energy": 0.9, "acousticness": 0.5})
    assert close > too_high


def test_recommend_songs_sorted_highest_first():
    songs = load_songs("data/songs.csv")
    results = recommend_songs({"genre": "lofi", "mood": "chill", "energy": 0.4}, songs, k=5)
    scores = [score for _, score, _ in results]
    assert len(results) == 5
    assert scores == sorted(scores, reverse=True)
    assert results[0][0]["genre"] == "lofi"


def test_diversity_penalty_avoids_repeat_artist_and_genre():
    from src.recommender import recommend_diverse
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    plain = [s["title"] for s, _, _ in recommend_songs(prefs, songs, k=5)]
    diverse = recommend_diverse(prefs, songs, k=5)
    titles = [s["title"] for s, _, _ in diverse]
    assert "Focus Flow" in plain          # LoRoom + lofi again
    assert "Focus Flow" not in titles     # pushed out by the penalty
    assert len(titles) == len(set(titles)) == 5


# ---- Optional challenges ---------------------------------------------------- #
def test_new_features_load_correctly():
    song = load_songs("data/songs.csv")[0]
    assert isinstance(song["popularity"], float)
    assert isinstance(song["mood_tags"], list)
    assert song["release_decade"].endswith("s")


def test_advanced_features_only_count_when_user_asks():
    song = {"genre": "jazz", "mood": "relaxed", "energy": 0.4, "acousticness": 0.5,
            "release_decade": "2010s", "mood_tags": ["cozy"], "popularity": 20.0,
            "instrumentalness": 0.8, "speechiness": 0.1}
    base = {"genre": "jazz", "mood": "relaxed", "energy": 0.4}
    plain, _ = score_song(base, song)
    extra, reasons = score_song({**base, "preferred_decade": "2010s", "mood_tags": ["cozy"],
                                 "popularity_pref": "underground", "focus_mode": True}, song)
    assert plain == 4.0
    assert extra > plain
    assert any("2010s" in r for r in reasons)
    assert any("mood tags cozy" in r for r in reasons)


def test_scoring_modes_change_the_ranking():
    from src.recommender import recommend_with_mode
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "indie", "mood": "sad", "energy": 0.9, "likes_acoustic": False}
    mood_top = recommend_with_mode(prefs, songs, "mood_first")[0][0]["title"]
    energy_top = recommend_with_mode(prefs, songs, "energy_focused")[0][0]["title"]
    assert mood_top == "Empty Platform"
    assert energy_top != "Empty Platform"


def test_mood_first_mode_matches_default_recommender():
    from src.recommender import recommend_with_mode
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    a = [s["title"] for s, _, _ in recommend_with_mode(prefs, songs, "mood_first")]
    b = [s["title"] for s, _, _ in recommend_songs(prefs, songs)]
    assert a == b
