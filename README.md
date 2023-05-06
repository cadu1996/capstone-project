# Rating Analysis of IMDb Data

A data engineering capstone project that analyzes IMDb data to identify the best and worst movies, shorts, animations, and other categories.

## Table of Contents

- [Introduction](#introduction)
- [Datasets](#datasets)
- [Data Dictionary](#data-dictionary)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Technology Choices and Justifications](#technology-choices-and-justifications)
- [Data Pipeline and Architecture](#data-pipeline-and-architecture)
- [Scenarios and Considerations](#scenarios-and-considerations)
- [Future Improvements](#future-improvements)

## Introduction

This capstone project aims to provide insights into various aspects of movies, such as their ratings and genres, by building a data warehouse and using data engineering techniques. The project utilizes IMDb datasets and implements a star schema data model to optimize query performance.

## Datasets

The project uses the following IMDb datasets:

1. `title.basics.tsv.gz`
2. `title.episode.tsv.gz`
3. `title.ratings.tsv.gz`

For detailed information about the datasets, including their attributes and data types, please refer to the [provided description](#user-content).

## Data Dictionary

This section provides a brief overview of the main attributes of the IMDb datasets used in this project.

### title.basics.tsv.gz

- `tconst`: Alphanumeric unique identifier of the title
- `titleType`: The type/format of the title (e.g., movie, short, tvseries, tvepisode, video, etc.)
- `primaryTitle`: The more popular title / the title used by the filmmakers on promotional materials at the point of release
- `originalTitle`: Original title, in the original language
- `isAdult`: 0 for non-adult titles; 1 for adult titles
- `startYear`: Release year of a title; for TV Series, it is the series start year
- `endYear`: TV Series end year; '\\N' for all other title types
- `runtimeMinutes`: Primary runtime of the title, in minutes
- `genres`: Up to three genres associated with the title

### title.episode.tsv.gz

- `tconst`: Alphanumeric identifier of the episode
- `parentTconst`: Alphanumeric identifier of the parent TV Series
- `seasonNumber`: Season number the episode belongs to
- `episodeNumber`: Episode number of the tconst in the TV series

### title.ratings.tsv.gz

- `tconst`: Alphanumeric unique identifier of the title
- `averageRating`: Weighted average of all the individual user ratings
- `numVotes`: Number of votes the title has received

## Getting Started

### Prerequisites

To set up and run the project, you will need:

- Docker and Docker-Compose installed
- At least 8 GB of RAM

### Installation

1. Install [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) on your system.

2. Clone the project repository:

   ```bash
   git clone https://github.com/your_username/your_project.git
   ```

3. Change to the project directory:

   ```bash
   cd your_project
   ```

4. Set up the required directories and environment variables (for Linux):

   ```bash
   mkdir -p ./dags ./logs ./plugins
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

5. Start Docker Compose:

   ```bash
   docker-compose up -d
   ```

6. Access Airflow at `http://localhost:8080`.

7. Log in to Airflow using the username and password `Airflow`.

8. Create a cluster in Amazon Redshift and an S3 Bucket.

9. Set up connections in Airflow for Amazon Redshift and the S3 Bucket:
   - Redshift: Create a new connection with the required credentials.
   - S3 Bucket: Set up the AWS credentials (access key and secret key) in Airflow.

10. Set up an HTTP connection in Airflow for IMDb datasets with the following hostname: `https://datasets.imdbws.com/`.

11. Enable the DAG in Airflow and configure it to run daily.

...

## Usage

Users can interact with the project by querying the data in the Amazon Redshift database.

## Sample Query and Results

### Example 1: Top 10 highest-rated Drama TV series

The following query retrieves the top 10 highest-rated TV series in the Drama genre, with at least 1000 votes:

```sql
WITH
    series AS (
        SELECT
            tconst,
            primaryTitle,
            startYear,
            endYear,
            runtimeMinutes
        FROM
            imdb.public.imdb_title_basics
        WHERE
            titleType = 'tvSeries'
            AND genres LIKE '%Drama%'
    ),
    ratings_filtered AS (
        SELECT
            tconst,
            averageRating,
            numVotes
        FROM
            imdb.public.imdb_title_ratings
        WHERE
            numVotes >= 1000
    ),
    episodes AS (
        SELECT
            parentTconst,
            COUNT(*) AS totalEpisodes
        FROM
            imdb.public.imdb_title_episode
        GROUP BY
            parentTconst
    )
SELECT
    s.tconst,
    s.primaryTitle,
    s.startYear,
    s.endYear,
    s.runtimeMinutes AS averageEpisodeRuntime,
    e.totalEpisodes,
    r.averageRating
FROM
    series s
    JOIN ratings_filtered r ON s.tconst = r.tconst
    JOIN episodes e ON s.tconst = e.parentTconst
ORDER BY
    r.averageRating DESC
LIMIT 10;
```

The query provided retrieves the top 10 highest-rated TV series in the Drama genre, with at least 1000 votes. The query returns the following information for each TV series:

- tconst: Unique identifier of the TV series
- primaryTitle: The primary title of the TV series
- startYear: The year the TV series started
- endYear: The year the TV series ended (if applicable)
- averageEpisodeRuntime: The average runtime (in minutes) of each episode
- totalEpisodes: The total number of episodes in the TV series
- averageRating: The average rating of the TV series

Here are the results:

| tconst     | primaryTitle                          | startYear | endYear | averageEpisodeRuntime | totalEpisodes | averageRating |
|------------|---------------------------------------|-----------|---------|-----------------------|---------------|---------------|
| tt0903747  | Breaking Bad                          | 2008      | 2013    | 49                    | 62            | 9.5           |
| tt15251018 | Sabka Sai                             | 2021      | 2021    | 42                    | 10            | 9.4           |
| tt0244911  | Malgudi Days                          | 1986      | 2006    |                       | 54            | 9.4           |
| tt3109682  | The Palestinian Alienation            | 2004      | 2004    |                       | 31            | 9.4           |
| tt7690588  | Sahodaraya                            | 2017      |         |                       | 38            | 9.3           |
| tt12392504 | Scam 1992: The Harshad Mehta Story    | 2020      | 2020    | 54                    | 10            | 9.3           |
| tt3109706  | Al-Zeer Salem                         | 2000      | 2001    |                       | 10            | 9.3           |
| tt2147999  | Devon Ke Dev... Mahadev               | 2011      | 2014    | 22                    | 816           | 9.3           |
| tt9471404  | The Chosen                            | 2017      |         | 54                    | 26            | 9.3           |
| tt0077051  | Matador                               | 1978      | 1982    | 67                    | 24            | 9.3           |

These are the top 10 highest-rated Drama TV series according to IMDb data, considering the given criteria.


### Example 2: Top 10 highest-rated Sci-Fi movies with a runtime of over 120 minutes

```sql
WITH
    movies AS (
        SELECT
            tconst,
            primaryTitle,
            startYear,
            runtimeMinutes
        FROM
            imdb.public.imdb_title_basics
        WHERE
            titleType = 'movie'
            AND genres LIKE '%Sci-Fi%'
            AND runtimeMinutes > 120
    ),
    ratings_filtered AS (
        SELECT
            tconst,
            averageRating,
            numVotes
        FROM
            imdb.public.imdb_title_ratings
        WHERE
            numVotes >= 1000
    )
SELECT
    m.tconst,
    m.primaryTitle,
    m.startYear,
    m.runtimeMinutes,
    r.averageRating,
    r.numVotes
FROM
    movies m
    JOIN ratings_filtered r ON m.tconst = r.tconst
ORDER BY
    r.averageRating DESC
LIMIT 10;
```

The query provided retrieves the top 10 highest-rated Sci-Fi movies with a runtime of over 120 minutes and at least 1000 votes. The query returns the following information for each movie:

- tconst: Unique identifier of the movie
- primaryTitle: The primary title of the movie
- startYear: The year the movie was released
- runtimeMinutes: The runtime (in minutes) of the movie
- averageRating: The average rating of the movie
- numVotes: The number of votes the movie has received

Here are the results:

| tconst     | primaryTitle                   | startYear | runtimeMinutes | averageRating | numVotes  |
|------------|--------------------------------|-----------|----------------|---------------|-----------|
| tt12820524 | Helsreach: The Movie           | 2019      | 150            | 9.1           | 1128      |
| tt1375666  | Inception                      | 2010      | 148            | 8.8           | 2403471   |
| tt0133093  | The Matrix                     | 1999      | 136            | 8.7           | 1950804   |
| tt0103064  | Terminator 2: Judgment Day     | 1991      | 137            | 8.6           | 1119446   |
| tt1795369  | Frankenstein                   | 2011      | 130            | 8.6           | 3980      |
| tt0816692  | Interstellar                   | 2014      | 169            | 8.6           | 1898240   |
| tt0252196  | Aditya 369                     | 1991      | 140            | 8.5           | 3196      |
| tt0482571  | The Prestige                   | 2006      | 130            | 8.5           | 1359649   |
| tt4154756  | Avengers: Infinity War         | 2018      | 149            | 8.4           | 1115760   |
| tt0090605  | Aliens                         | 1986      | 137            | 8.4           | 730355    |


## Technology Choices and Justifications

The project uses the following tools and technologies:

- **Python:** The primary programming language, chosen for its extensive libraries and support for data engineering tasks.
- **Apache Airflow:** Orchestrates the data pipeline, providing a robust, scalable, and easy-to-maintain solution for managing complex data workflows.
- **Amazon Redshift:** The database used in the project, selected for its ability to handle large-scale datasets, compatibility with Amazon S3, and strong performance for analytical queries.
- **Amazon S3:** Provides data storage, offering high scalability, durability, and availability.

The star schema data model was designed to provide a comprehensive view of IMDb data while being optimized for analytical queries related to movie ratings, genres, and other aspects. This schema allows for efficient querying and aggregations, reducing the need for complex joins and improving query performance.

## Data Pipeline and Architecture

A data warehouse was built to store the IMDb data, using a star schema to optimize query performance. The data pipeline was orchestrated using Apache Airflow, and the data was fetched from IMDb and stored in an Amazon S3 bucket. The data was then loaded into an Amazon Redshift database for further analysis.

## Scenarios and Considerations

In the event of different scenarios, the project can be approached as follows:

1. **If the data was increased by 100x:**
   - Scale the Amazon S3 and Redshift storage capacity.
   - Optimize data processing and loading procedures.
   - Consider using Spark or other distributed data processing frameworks.
2. **If the pipelines were to be run on a daily basis by 7 am every day:**
   - Schedule the Apache Airflow DAG to run daily at a specific time.
   - Implement data validation checks and monitoring.
3. **If the database needed to be accessed by 100+ people:**
   - Configure Amazon Redshift to handle increased user connections and load.
   - Implement caching mechanisms and query optimization techniques to ensure optimal performance.

## Future Improvements

In the future, the project could be expanded by integrating data from other sources, such as Reddit and Twitter, to analyze movie sentiment and discover lesser-known but highly-rated movies. Additionally, a data lake architecture could be implemented to provide more flexibility and scalability for data storage and processing.
