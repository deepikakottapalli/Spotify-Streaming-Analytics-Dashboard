import pandas as pd

def main():
    df = load_data("spotify_artist_streaming_2020_2025.csv")
    print(get_summary_stats(df))

def load_data(path):
    return pd.read_csv(path, parse_dates=['release_date'])

def get_summary_stats(df):
    return {
        "total_tracks":len(df),
        "total_artists":df["artist_name"].nunique(),
        "average_popularity":round(df["popularity"].mean(), 3),
        "total_streams":df["stream_count"].sum(),
    }

def top_artists(df, n=10):
    group = df.groupby("artist_name")["stream_count"].sum()
    grouped = group.sort_values(ascending=False)
    return grouped.head(n)

def genre_breakdown(df):
    group = df.groupby("genre")["stream_count"].sum()
    grouped = group.sort_values(ascending=False)
    return grouped

def popularity_trend(df):
    group = df.groupby(df["release_date"].dt.year)["stream_count"].sum()
    return group

def popularity_trend_monthly(df):
    group = df.groupby(df["release_date"].dt.to_period("M"))["stream_count"].sum()
    return group

if __name__ == "__main__":
    main()
