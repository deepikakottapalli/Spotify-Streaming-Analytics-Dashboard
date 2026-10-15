# 🎧 Spotify Streaming Analytics Dashboard

#### Video Demo: https://youtu.be/RuJZXqm22aU?si=a-KIkJSiHt-8faXe

<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/fc2e1e56-c7ba-445c-b233-45ada0374b8f" />


#### Description:
An interactive Python dashboard exploring artist streams, genre trends, and audio features across **50,000 tracks (2020–2025)**. Built using `pandas` for pipeline data processing, `Plotly` for interactive visualizations, and `Streamlit` for the web UI.

Users can filter the dataset by genre, artist, and release date range. The UI instantly updates dynamic summary statistics (KPI cards) and four core visualizations:
* **Top 10 Artists:** Bar chart of total streams.
* **Genre Breakdown:** Donut chart of stream proportions.
* **Streaming Trends:** Monthly time-series line graph.
* **Popularity vs. Danceability:** Scatter plot comparing popularity against danceability, colored by genre, sized by stream count

Additional features include a collapsible data explorer displaying up to 500 color-coded raw tracks and CSV download buttons for the top artists and genre breakdown data.

---

## Why This Project
I'm a third-year Computer Science (Data Science) student aiming toward data analyst and, longer-term, AI engineer roles. I wanted my final project to reflect that direction, so I chose to build a real, interactive analytics dashboard. This let me practice an end-to-end analyst workflow: loading and cleaning data, aggregating it meaningfully, and presenting it through an interface a non-technical viewer could actually use.

---

## Files

* **`project.py`** — Core data processing logic, kept completely separate from the UI layer so it can be tested independently:
  * `main()` — loads the dataset and prints summary stats when run directly.
  * `load_data(path)` — reads the CSV into a pandas DataFrame, parsing `release_date` as a proper datetime.
  * `get_summary_stats(df)` — Calculates and returns metrics (tracks, unique artists, mean popularity, aggregate streams) as a dictionary.
  * `top_artists(df, n=10)` — returns the top n artists by total streams, sorted descending.
  * `genre_breakdown(df)` — returns total streams grouped by genre, sorted descending.
  * `popularity_trend(df)` — returns total streams grouped by year.
  * `popularity_trend_monthly(df)` — returns total streams grouped by month, used for the dashboard's time series chart.
* **`test_project.py`** — `pytest` tests for every function above, run against a small hand-built fake DataFrame (not the real CSV) so expected results can be verified by hand rather than trusted blindly.
* **`app.py`** — the `Streamlit` dashboard itself. Handles multi-select filtering, state management, KPI rendering, and Plotly execution via `st.plotly_chart`.
* **`spotify_artist_streaming_2020_2025.csv`** — Cleaned 50,000-row Kaggle source dataset containing 33 feature columns.
* **`requirements.txt`** — Explicit Python library dependencies.

---

## Key Design Decisions

* **Logic & UI Separation:** All calculations in `project.py` are pure functions. `app.py` strictly manages layout, routing, and user input. This ensures the data logic can be evaluated, packaged, or migrated independently.
* **Synthetic Testing:** `test_project.py` evaluates code against hardcoded, hand-verified mock tables rather than the production CSV. This guarantees deterministic testing states.
* **Flat Data Visualization:** Avoided nested layout engines (like Treemaps) because the underlying schema lacks deep hierarchical categorization. Four flat views maximize visual clarity without forcing false relationships.
* **Chained Filter Execution:** Implemented a single-pass processing pipeline (`df → df2 → df3 → filtered_df`). This guarantees that concurrent sidebar selections narrow data correctly without state overwrites.

---

## Installation & Execution

### 1. Install Dependencies
Install all required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 2. Launch the Dashboard
Run the Streamlit application server local host:
```bash
streamlit run app.py
```

### 3. Run the Core Script Directly
To view summary statistics printed to your console:
```bash
python project.py
```

### 4. Execute Test Suite
Run the automated tests to verify function integrity:
```bash
pytest test_project.py
```

## Data Source

Dataset: [Spotify Streaming Data and Audio Features (2020-2025)](https://www.kaggle.com/datasets/beamhonor0911/spotify-artist-streaming-analytics-20202025) via Kaggle.
