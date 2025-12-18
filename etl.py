import os
import re
import time
import sqlite3
import requests
import pandas as pd


DATABASE_PATH = "movies.db"

MOVIES_CSV_PATH = "data/movies.csv"
RATINGS_CSV_PATH = "data/ratings.csv"

OMDB_API_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

MAX_API_CALLS = 50
API_DELAY = 0.5


def extract_data():
    movies_df = pd.read_csv(MOVIES_CSV_PATH)
    ratings_df = pd.read_csv(RATINGS_CSV_PATH)

    print(f"Movies loaded: {len(movies_df)}")
    print(f"Ratings loaded: {len(ratings_df)}")

    return movies_df, ratings_df


def extract_year(title):
    match = re.search(r"\((\d{4})\)", title)
    return int(match.group(1)) if match else None


def clean_title(title):
    return re.sub(r"\s*\(\d{4}\)", "", title).strip()


def fetch_omdb_data(title, year):
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
    movies_df["release_year"] = movies_df["title"].apply(extract_year)
    movies_df["clean_title"] = movies_df["title"].apply(clean_title)

    omdb_results = {}
    api_calls = 0

    if OMDB_API_KEY:
        for _, row in movies_df.iterrows():
            if api_calls >= MAX_API_CALLS:
                break

            details = fetch_omdb_data(row["clean_title"], row["release_year"])
            if details:
                omdb_results[row["movieId"]] = details

            api_calls += 1
            time.sleep(API_DELAY)

    movies_df["imdb_id"] = movies_df["movieId"].map(
        lambda x: omdb_results.get(x, {}).get("imdb_id")
    )
    movies_df["director"] = movies_df["movieId"].map(
        lambda x: omdb_results.get(x, {}).get("director")
    )
    movies_df["plot"] = movies_df["movieId"].map(
        lambda x: omdb_results.get(x, {}).get("plot")
    )
    movies_df["box_office"] = movies_df["movieId"].map(
        lambda x: omdb_results.get(x, {}).get("box_office")
    )

    return movies_df


def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    with open("schema.sql", "r") as file:
        conn.executescript(file.read())
    conn.close()


def load_movies(conn, movies_df):
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
    genres = set()
    movie_genres = []

    for _, row in movies_df.iterrows():
        if pd.notna(row["genres"]):
            for genre in row["genres"].split("|"):
                genres.add(genre)
                movie_genres.append((row["movieId"], genre))

    conn.executemany(
        "INSERT OR IGNORE INTO genres (genre_name) VALUES (?)",
        [(g,) for g in genres]
    )

    conn.executemany("""
        INSERT OR IGNORE INTO movie_genres (movie_id, genre_id)
        SELECT ?, genre_id FROM genres WHERE genre_name = ?
    """, movie_genres)


def load_ratings(conn, ratings_df):
    ratings = ratings_df[
        ["userId", "movieId", "rating", "timestamp"]
    ].values.tolist()

    conn.executemany("""
        INSERT OR IGNORE INTO ratings
        (user_id, movie_id, rating, timestamp)
        VALUES (?, ?, ?, ?)
    """, ratings)


def run_etl():
    movies_df, ratings_df = extract_data()

    print("Processing... please wait.")

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
