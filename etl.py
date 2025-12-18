import pandas as pd
import sqlite3
import requests
import os
import re
import time

# ================= CONFIGURATION ================= #

DATABASE_PATH = "movies.db"
MOVIES_CSV_PATH = "data/movies.csv"
RATINGS_CSV_PATH = "data/ratings.csv"

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = "http://www.omdbapi.com/"

MAX_API_CALLS = 50     # Free-tier safe limit
API_DELAY = 0.5          # Delay between API calls (seconds)

# ================= EXTRACT ================= #

def extract_data():
    """Extract movies and ratings from CSV files"""
    print("Extracting data from CSV files...")

    movies_df = pd.read_csv(MOVIES_CSV_PATH)
    ratings_df = pd.read_csv(RATINGS_CSV_PATH)

    print(f"Movies loaded: {len(movies_df)}")
    print(f"Ratings loaded: {len(ratings_df)}")

    return movies_df, ratings_df

# ================= TRANSFORM ================= #

def extract_year(title):
    """Extract release year from movie title"""
    match = re.search(r"\((\d{4})\)", title)
    return int(match.group(1)) if match else None

def clean_title(title):
    """Remove year from movie title"""
    return re.sub(r"\s*\(\d{4}\)", "", title).strip()

def fetch_omdb_data(title, year):
    """Fetch movie details from OMDb API"""
    if not OMDB_API_KEY:
        return None

    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "y": year
    }

    try:
        response = requests.get(OMDB_API_URL, params=params, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            return {
                "imdb_id": data.get("imdbID"),
                "director": data.get("Director"),
                "plot": data.get("Plot"),
                "box_office": data.get("BoxOffice")
            }
    except Exception:
        pass

    return None

def transform_data(movies_df):
    """Clean and enrich movie data"""
    print("Transforming movie data...")

    movies_df["release_year"] = movies_df["title"].apply(extract_year)
    movies_df["clean_title"] = movies_df["title"].apply(clean_title)

    omdb_results = {}
    api_count = 0

    if OMDB_API_KEY:
        print(f"Enriching movie data from OMDb API (max {MAX_API_CALLS} movies)...")

        for _, row in movies_df.iterrows():
            if api_count >= MAX_API_CALLS:
                break

            details = fetch_omdb_data(row["clean_title"], row["release_year"])
            if details:
                omdb_results[row["movieId"]] = details

            api_count += 1
            time.sleep(API_DELAY)

        print(f"OMDb enrichment completed for {api_count} movies")
    else:
        print("OMDb API key not set. Skipping enrichment step.")

    movies_df["imdb_id"] = movies_df["movieId"].map(lambda x: omdb_results.get(x, {}).get("imdb_id"))
    movies_df["director"] = movies_df["movieId"].map(lambda x: omdb_results.get(x, {}).get("director"))
    movies_df["plot"] = movies_df["movieId"].map(lambda x: omdb_results.get(x, {}).get("plot"))
    movies_df["box_office"] = movies_df["movieId"].map(lambda x: omdb_results.get(x, {}).get("box_office"))

    return movies_df

# ================= LOAD ================= #

def create_tables():
    """Create database tables using schema.sql"""
    print("Creating database tables...")

    conn = sqlite3.connect(DATABASE_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

def load_movies(conn, movies_df):
    """Load movies table"""
    movies = movies_df[
        ["movieId", "clean_title", "release_year",
         "imdb_id", "director", "plot", "box_office"]
    ].values.tolist()

    conn.executemany("""
        INSERT OR IGNORE INTO movies
        (movie_id, title, release_year, imdb_id, director, plot, box_office)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, movies)

def load_genres(conn, movies_df):
    """Load genres and movie_genres tables"""
    genres = set()
    movie_genres = []

    for _, row in movies_df.iterrows():
        if pd.notna(row["genres"]):
            for genre in row["genres"].split("|"):
                genres.add(genre)
                movie_genres.append((row["movieId"], genre))

    conn.executemany("""
        INSERT OR IGNORE INTO genres (genre_name)
        VALUES (?)
    """, [(g,) for g in genres])

    conn.executemany("""
        INSERT OR IGNORE INTO movie_genres (movie_id, genre_id)
        SELECT ?, genre_id FROM genres WHERE genre_name = ?
    """, movie_genres)

def load_ratings(conn, ratings_df):
    """Load ratings table"""
    ratings = ratings_df[
        ["userId", "movieId", "rating", "timestamp"]
    ].values.tolist()

    conn.executemany("""
        INSERT OR IGNORE INTO ratings
        (user_id, movie_id, rating, timestamp)
        VALUES (?, ?, ?, ?)
    """, ratings)

# ================= PIPELINE ================= #

def run_etl():
    print("Starting ETL pipeline...")

    movies_df, ratings_df = extract_data()
    movies_df = transform_data(movies_df)

    create_tables()

    conn = sqlite3.connect(DATABASE_PATH)
    load_movies(conn, movies_df)
    load_genres(conn, movies_df)
    load_ratings(conn, ratings_df)
    conn.commit()
    conn.close()

    print("ETL pipeline completed successfully!")

if __name__ == "__main__":
    run_etl()
