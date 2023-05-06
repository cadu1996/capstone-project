class SqlQueries:

    imdb_title_basics_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_basics (
            tconst VARCHAR(255) NOT NULL,
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
            tconst VARCHAR(255) NOT NULL,
            averageRating FLOAT,
            numVotes INTEGER
        );
    """)

    imdb_title_crew_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_crew (
            tconst VARCHAR(255) NOT NULL,
            directors VARCHAR(MAX),
            writers VARCHAR(MAX)    
        );
    """)

    imdb_title_principals_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_principals (
            tconst VARCHAR(255) NOT NULL,
            ordering INTEGER,
            nconst VARCHAR(255),
            category VARCHAR(255),
            job VARCHAR(255),
            characters VARCHAR(MAX)
        );
    """)

    imdb_name_basics_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_name_basics (
            nconst VARCHAR(255) NOT NULL,
            primaryName VARCHAR(255),
            birthYear INTEGER,
            deathYear INTEGER,
            primaryProfession VARCHAR(255),
            knownForTitles VARCHAR(255)
        );
    """)

    imdb_title_episode_create = ("""
        CREATE TABLE IF NOT EXISTS public.imdb_title_episode (
            tconst VARCHAR(255) NOT NULL,
            parentTconst VARCHAR(255),
            seasonNumber INTEGER,
            episodeNumber INTEGER
        );
    """)

