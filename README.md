### Movie Data Pipeline (ETL Project)

## Overview

This project is a simple ETL (Extract, Transform, Load) data pipeline built using Python, SQLite, and the OMDb API.

The goal of this project is to demonstrate foundational data engineering concepts such as:

- Data ingestion
- Data transformation
- API-based enrichment
- Relational data modeling

# Movie Data Pipeline – Data Engineering Assignment

## Objective

The objective of this assignment is to design and build a simple data pipeline that:

- Ingests movie data from multiple sources
- Cleans and transforms the data
- Enriches it using an external API
- Loads it into a relational database
- Answers analytical questions using SQL

This project simulates a real-world data engineering task commonly performed in analytics and data platform teams.

## Technologies Used

- Python 3
- Pandas – data processing and transformation
- SQLite – relational database
- OMDb API – external movie metadata enrichment
- DB Browser for SQLite – database inspection and query execution

## Assignment Tasks and Implementation

### Task 1: Environment Setup

#### What was done

- Created a Python virtual environment for dependency isolation
- Installed required Python libraries (pandas, requests)
- Selected SQLite as the relational database (lightweight and free)
- Structured the project according to the submission guidelines

#### Outcome

- Clean and reproducible development environment
- Ready for ETL pipeline execution

### Task 2: Data Sources

#### 1. Local CSV Files

- Used the MovieLens small dataset

Processed the following files:

- `movies.csv` – movie metadata
- `ratings.csv` – user ratings

These files act as the primary raw data source.

#### 2. External API – OMDb

- Integrated the OMDb API to enrich movie data

Retrieved additional attributes:

- IMDb ID
- Director
- Plot
- Box Office collection

### Task 3: Data Modeling

#### What was done

- Designed a relational database schema
- Created normalized tables to avoid data duplication
- Implemented relationships using primary and foreign keys

#### Tables Created

- `movies` – movie-level information
- `genres` – unique genres
- `movie_genres` – many-to-many relationship between movies and genres
- `ratings` – user ratings

The schema is defined in `schema.sql`.

### Task 4: ETL Pipeline Implementation (etl.py)

The ETL pipeline is implemented in Python and follows a clear Extract → Transform → Load flow.

#### Extract

- Reads `movies.csv` and `ratings.csv`
- Loads data into Pandas DataFrames
- Performs basic validation

#### Transform

- Extracts release year from movie titles
- Cleans movie titles
- Splits genre data for normalization
- Enriches movie data using OMDb API
- Handles missing or unavailable API responses safely

##### API Rate Limiting

To respect the OMDb free tier limits:

```
MAX_API_CALLS = 50
```

- Only the first 50 movies are enriched
- All movies are still stored in the database
- Non-enriched movies contain NULL values for API fields

This demonstrates responsible API usage, as expected in production systems.

#### Load

- Creates tables using `schema.sql`
- Inserts transformed data into SQLite
- Stores final output in `movies.db`

The pipeline can be safely re-run.

### Task 5: Analytical Queries (queries.sql)

After loading the data, SQL queries were written to answer the following questions:

- Which movie has the highest average rating?
- What are the top 5 movie genres with the highest average rating?
- Which director has the most movies in the dataset?
- What is the average rating of movies released each year?

These queries are stored in `queries.sql`.

## Secure API Key Handling

The OMDb API key is not hard-coded

It is read using an environment variable:

```
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
```

### Why this approach is used

- Prevents exposing sensitive credentials
- Follows industry security best practices
- Safe for GitHub and project sharing

## Viewing Results

Open `movies.db` using DB Browser for SQLite

- Use Browse Data to inspect tables
- Use Execute SQL to run queries from `queries.sql`

SQL execution is required only for analysis, not for data loading.

## Key Highlights

- Clear ETL pipeline design
- Secure handling of API credentials
- Controlled external API usage
- Normalized relational data model
- Clean, readable, and well-documented code


## How to Run the Project (Step-by-Step Commands)

### Step 1: Open Project Folder

Open Command Prompt / PowerShell and navigate to the project directory:

```
cd C:\Works\movie-data-pipeline
```
the path differs from pc to pc - so check for your specified path.

### Step 2: Create and Activate Virtual Environment

Create a virtual environment:

```
python -m venv venv
```

Activate the virtual environment:

```
venv\Scripts\activate
```

You should see (venv) in the terminal.

### Step 3: Install Required Dependencies

```
pip install -r requirements.txt
```

### Step 4: Set OMDb API Key (One-Time Setup)

Set the OMDb API key as an environment variable (Windows):

```
setx OMDB_API_KEY "your_api_key_here"
```

⚠️ Important:

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

⚠️ Note:

You do not need to run SQL to load data
SQL is used only for analysis and verification

## New README file
