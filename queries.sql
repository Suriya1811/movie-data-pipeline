-- 1. Movie with the highest average rating
SELECT 
    m.title,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.movie_id
ORDER BY avg_rating DESC
LIMIT 1;


-- 2. Top 5 genres with highest average rating
SELECT 
    g.genre_name,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN ratings r ON mg.movie_id = r.movie_id
GROUP BY g.genre_id
ORDER BY avg_rating DESC
LIMIT 5;


-- 3. Director with the most movies
SELECT 
    director,
    COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;


-- 4. Average rating by release year
SELECT 
    m.release_year,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;
