# Movie Data Pipeline (ETL Project)

## Overview

This project implements a simple end-to-end ETL (Extract, Transform, Load) pipeline using Python.
The pipeline ingests movie and rating data from CSV files, enriches movie metadata using the OMDb API, stores the processed data in a relational database, and enables analytical queries using SQL.

The purpose of this project is to demonstrate core data engineering fundamentals, including data ingestion, data transformation, external API integration, and relational data modeling.

## Objective

The objective of this assignment is to design and build a small but realistic data pipeline that:

- Ingests movie data from multiple sources
- Cleans and transforms raw data
- Enriches movie metadata using an external API
- Loads structured data into a relational database
- Supports analytical queries using SQL


## Technologies Used

- Python 3 – core programming language
- Pandas – data ingestion and transformation
- SQLite – lightweight relational database
- OMDb API – external movie metadata enrichment
- DB Browser for SQLite – database inspection and query execution

## Task 1: Environment Setup

### What the assignment asked

- Choose a relational database
- Set up the database and required tables
- Write ingestion and transformation logic in Python

### What I did

- Selected SQLite as the relational database because it is lightweight, free, and well-suited for a take-home assignment.
- Created all required database tables using an SQL script (schema.sql).
- Implemented the complete ingestion and transformation logic using Python.
- Used standard libraries:
  - pandas for data ingestion and transformation
  - requests for external API calls
  - sqlite3 for database interaction

### Short Summary

SQLite was chosen for simplicity and reproducibility, while Python with Pandas and Requests was used to handle all ingestion and transformation logic in a clean and modular way.

## Task 2: Data Sources

### What the assignment asked

- Use two data sources:
  - Local CSV files (MovieLens dataset)
  - External OMDb API

### 2.1 Local CSV Files (MovieLens Dataset)

#### What I did

- Downloaded the MovieLens small dataset
- Used only:
  - movies.csv
  - ratings.csv
- Organized both files under a /data folder
- Loaded the data into Pandas DataFrames during the extract phase

#### Short Summary

The MovieLens dataset serves as the primary source of movie titles, genres, and user ratings.

### 2.2 External API – OMDb

#### What I did

- Generated a free OMDb API key
- Stored the API key securely using an environment variable
- Enriched movie data with:
  - IMDb ID
  - Director
  - Plot
  - Box office collection

#### Short Summary

The OMDb API acts as an external enrichment layer that adds additional movie metadata not available in the raw dataset.

## Task 3: Data Modeling

### What the assignment asked

- Design a simple database schema
- Handle relationships between movies, genres, and ratings
- Create schema.sql

### What I did

- Designed a normalized relational schema with four tables:
  - movies – movie-level information and enriched metadata
  - genres – unique genre values
  - movie_genres – many-to-many relationship between movies and genres
  - ratings – user ratings stored as a fact table
- Primary and foreign keys are used to maintain referential integrity.

### Short Summary

The schema is normalized to avoid duplication and structured to support efficient analytical queries.

## Task 4: Building the ETL Pipeline (etl.py)

This is the core of the assignment.

### 4.1 Extract Phase

#### What the assignment asked

- Read CSV files
- Fetch additional details from OMDb
- Handle missing or unmatched API results

#### What I did

- Read movies.csv and ratings.csv using Pandas
- Logged record counts to validate ingestion
- Queried OMDb using cleaned movie titles and release years
- Returned NULL values when API data was missing instead of failing the pipeline

#### Short Summary

The extract phase loads structured CSV data and treats the external API as an optional enrichment source.

### 4.2 Transform Phase

#### What the assignment asked

- Clean data
- Enrich data
- Feature engineering (bonus)

#### What I did

- Extracted release year from movie titles using regex
- Cleaned movie titles for better API matching
- Split genre strings (| separated) for normalization
- Enriched movies using OMDb responses
- Allowed NULL values where enrichment was unavailable
- Bonus Feature Engineering
  - Normalized genres into a separate table
  - Derived release_year from movie titles

#### Short Summary

Transformation focuses on data cleanliness, structured fields, and safe enrichment without breaking the pipeline.

### 4.3 API Handling and Rate Limiting

#### What the assignment warned about

- API mismatches
- Rate limits
- Missing data

#### What I did

- Limited API calls using:
  ```
  MAX_API_CALLS = 50
  ```
- Added a delay between API requests
- Ensured the pipeline continues even if the API fails

#### Short Summary

API usage is rate-limited and failure-tolerant to reflect real-world external dependency handling.

### 4.4 Load Phase

#### What the assignment asked

- Load transformed data
- Ensure idempotency

#### What I did

- Created tables using schema.sql
- Inserted data using INSERT OR IGNORE
- Ensured the pipeline can be safely re-run without duplicate records

#### Short Summary

The load phase is idempotent, allowing the pipeline to be re-run safely.

## Task 5: Analytical Queries (queries.sql)

### What the assignment asked

- Answer analytical questions using SQL.

### What I did

- Created SQL queries to answer:
  - Movie with the highest average rating
  - Top 5 genres by average rating
  - Director with the most movies
  - Average rating of movies released each year
- All queries are stored in queries.sql.

### Important Note

Director-related results depend on OMDb enrichment. Since API calls are limited, some results may be NULL, which is expected.

### Short Summary

The queries are logically correct and demonstrate how the data model supports analytical use cases.

## Conclusion

I completed all assignment tasks by building a clean, modular ETL pipeline that ingests CSV data, enriches it using a controlled external API, loads it into a normalized relational database, and supports analytical queries using SQL.


## How to Run the Project (Step-by-Step Commands)

### Step 1: Open Project Folder

Open Command Prompt / PowerShell and navigate to the project directory:

```
cd C:\Works\movie-data-pipeline
```

 Note: The path differs from PC to PC – adjust the path based on your system.

### Step 2: Create and Activate Virtual Environment

Create a virtual environment:

```
python -m venv venv
```

Activate the virtual environment:

```
venv\Scripts\activate
```

You should see `(venv)` in the terminal.

### Step 3: Install Required Dependencies

```
pip install -r requirements.txt
```

### Step 4: Set OMDb API Key (One-Time Setup)

Set the OMDb API key as an environment variable (Windows):

```
setx OMDB_API_KEY "your_api_key_here" - I added my API key to the Virtual Enviroinment, so it won't be public.

```

 Important:

- This command needs to be run only once
- Restart the terminal after setting the key
- The API key is not written inside the code

### Step 5: Run the ETL Pipeline

Execute the ETL process:

```
python etl.py
```

This command performs:

- Extract → reads CSV files
- Transform → cleans and enriches data
- Load → stores data into SQLite

After successful execution, a file named `movies.db` will be created.

### Step 6: View Output Using DB Browser for SQLite (No Command Needed)

Open DB Browser for SQLite

Click Open Database

Select:

```
C:\Works\movie-data-pipeline\movies.db
```

Use:

- Browse Data → to view tables
- Execute SQL → to run queries from `queries.sql`

 Note:

- You do not need to run SQL to load data
- SQL is used only for analysis and verification
