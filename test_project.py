import pandas as pd

from project import load_data, get_summary_stats, top_artists, genre_breakdown, popularity_trend, popularity_trend_monthly
import pytest

def fake_data():
    data = {
        "artist_name": ["A", "B", "C", "B", "A"],
        "popularity": [80, 40, 90, 40, 20],
        "stream_count": [1000, 900, 1800, 800, 350],
        "genre": ["Pop", "R&B", "Pop", "Jazz", "R&B"],
        "release_date": pd.to_datetime(["2024-10-26", "2023-01-31", "2022-12-02", "2020-01-05", "2024-04-30"])
    }

    return pd.DataFrame(data)

def test_get_summary_stats():
    df = fake_data()
    stats = get_summary_stats(df)
    assert stats["total_artists"] == 3
    assert stats["total_streams"] == 4850
    assert stats["average_popularity"] == 54

def test_top_artists():
    df = fake_data()
    artists = top_artists(df)
    assert artists["C"] == 1800
    assert artists["A"] == 1350
    assert artists["B"] == 1700

def test_genre_breakdown():
    df = fake_data()
    genre = genre_breakdown(df)
    assert genre["Pop"] == 2800
    assert genre["R&B"] == 1250
    assert genre["Jazz"] == 800

def test_popularity_trend():
    df = fake_data()
    trend = popularity_trend(df)
    assert trend[2020] == 800
    assert trend[2022] == 1800
    assert trend[2023] == 900
    assert trend[2024] == 1350

def test_popularity_trend_monthly():
    df = fake_data()
    trend_monthly = popularity_trend_monthly(df)
    assert trend_monthly["Oct 2024"] == 1000
    assert trend_monthly["Dec 2022"] == 1800
    assert trend_monthly["Jan 2020"] == 800
