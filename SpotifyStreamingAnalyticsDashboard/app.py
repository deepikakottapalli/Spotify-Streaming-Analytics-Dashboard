import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="Spotify Streaming Analytics", page_icon=":headphones:", layout="wide")
st.title(":headphones: Spotify Streaming Analytics")
st.markdown("_Exploring artist streams, genres, and audio trends, 2020–2025_")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

from project import load_data, get_summary_stats, top_artists, genre_breakdown, popularity_trend, popularity_trend_monthly

@st.cache_data
def get_data():
    return load_data("spotify_artist_streaming_2020_2025.csv")
df = get_data()

col1, col2 = st.columns((2))
df["release_date"] = pd.to_datetime(df["release_date"])

startDate = pd.to_datetime(df["release_date"]).min()
endDate = pd.to_datetime(df["release_date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

st.sidebar.header("Choose your filter: ")

# Filter the data based on Genres
genres = st.sidebar.multiselect("Pick your Genre", df["genre"].unique(), default=df["genre"].unique())
if not genres:
    df2 = df.copy()
else:
    df2 = df[df["genre"].isin(genres)]

# Filter the data based on Artists
artist = st.sidebar.multiselect("Pick your Artist", df["artist_name"].unique(), default=df["artist_name"].unique())
if not artist:
    df3 = df2.copy()
else:
    df3 = df2[df2["artist_name"].isin(artist)]

# Filter by release date range
mask = (df3["release_date"] >= pd.to_datetime(startDate)) & (df3["release_date"] <= pd.to_datetime(endDate))
filtered_df = df3[mask]

stats = get_summary_stats(filtered_df)

# KPI rows
col1, col2, col3, col4 = st.columns(4, gap="medium")
with col1:
    st.metric("Total Tracks", stats["total_tracks"], icon=":material/music_note:", border=True)
with col2:
    st.metric("Total Artists", stats["total_artists"], icon=":material/mic:", border=True)
with col3:
    st.metric("Average Popularity", stats["average_popularity"], icon=":material/star:", border=True)
with col4:
    st.metric("Total Streams", f"{stats["total_streams"]:,}", icon=":material/play_circle:", border=True)

st.divider()
col1, col2 = st.columns(2, gap="large")

# Bar Chart
with col1:
    st.subheader("Top 10 Artists by Streams")
    top = top_artists(filtered_df)
    fig = px.bar(top, x = top.index, y = top.values, text = top.values, template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)

# Pie Chart
with col2:
    st.subheader("Streams by Genre")
    genres_data = genre_breakdown(filtered_df)
    fig = px.pie(genres_data, values=genres_data.values, names=genres_data.index, hole=0.5)
    st.plotly_chart(fig,use_container_width=True)

# Download Data
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Artists_ViewData"):
        st.write(top)
        csv = top.to_csv().encode("utf-8")
        st.download_button("Download Data", data = csv, file_name = "artists.csv", mime = "text/csv",
                           help = "Click here to download the data as a CSV file")
with cl2:
    with st.expander("Genres_ViewData"):
        st.write(genres_data)
        csv = genres_data.to_csv().encode("utf-8")
        st.download_button("Download Data", data = csv, file_name = "genres.csv", mime = "text/csv",
                           help = "Click here to download the data as a CSV file")

# Time Series Analysis
trend = popularity_trend_monthly(filtered_df)
trend_df = trend.reset_index()
trend_df.columns = ["month_year", "stream_count"]
trend_df["month_year"] = trend_df["month_year"].dt.to_timestamp().dt.strftime("%b %Y")

st.subheader('Time Series Analysis')

fig2 = px.line(trend_df,
               x = "month_year",
               y = "stream_count",
               labels = {"month_year" : "Month", "stream_count" : "Number of Streams"},
               height = 500,
               width = 1000,
               template = "gridon")
fig2.update_xaxes(type="category")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(trend_df.T.style.background_gradient(cmap="Blues"))
    csv = trend_df.to_csv().encode("utf-8")
    st.download_button("Download Data", data = csv, file_name = "TimeSeries.csv", mime = "text/csv",
                               help = "Click here to download the data as a CSV file")

# Scatter plot

st.header("Popularity vs Danceability")
fig3 = px.scatter(filtered_df,
                  x = "danceability",
                  y = "popularity",
                  color = "genre",
                  size = "stream_count",
                  hover_data = ["track_name", "artist_name"],
                  opacity = 0.5,
                  template="plotly_dark"
                  )
fig3.update_traces(marker=dict(line=dict(width=0)))
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

csv = df.to_csv().encode("utf-8")
st.download_button("Download Data", data = csv, file_name = "Data.csv", mime = "text/csv",
                               help = "Click here to download the data as a CSV file")
