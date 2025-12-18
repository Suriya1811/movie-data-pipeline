-- =========================
-- Movies table
-- =========================
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INTEGER,
    imdb_id TEXT UNIQUE,
    director TEXT,
    plot TEXT,
    box_office TEXT
);

-- =========================
-- Genres table
-- =========================
CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT UNIQUE NOT NULL
);

-- =========================
-- Movie ↔ Genre mapping
-- =========================
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

-- =========================
-- Ratings table
-- =========================
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL NOT NULL,
    timestamp INTEGER,
    PRIMARY KEY (user_id, movie_id, timestamp),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
