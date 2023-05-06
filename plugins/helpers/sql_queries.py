class SqlQueries:

    imdb_title_basics_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_basics (
            tconst VARCHAR(255) PRIMARY KEY,
            titleType VARCHAR(255),
            primaryTitle VARCHAR(MAX),
            originalTitle VARCHAR(MAX),
            isAdult INTEGER,
            startYear INTEGER,
            endYear INTEGER,
            runtimeMinutes INTEGER,
            genres VARCHAR(255)
        );
    """)

    imdb_title_ratings_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_ratings (
            tconst VARCHAR(255) PRIMARY KEY,
            averageRating FLOAT,
            numVotes INTEGER
        );
    """)

    imdb_title_episode_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_episode (
            tconst VARCHAR(255) PRIMARY KEY,
            parentTconst VARCHAR(255),
            seasonNumber INTEGER,
            episodeNumber INTEGER
        );
    """)


