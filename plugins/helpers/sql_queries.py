class SqlQueries:

    staging_imdb_title_basics_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_imdb_title_basics (
            tconst VARCHAR(255) NOT NULL,
            titleType VARCHAR(255),
            primaryTitle VARCHAR(255),
            originalTitle VARCHAR(255),
            isAdult INTEGER,
            startYear INTEGER,
            endYear INTEGER,
            runtimeMinutes INTEGER,
            genres VARCHAR(255)
        );
    """)

    staging_imdb_title_ratings_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_imdb_title_ratings (
            tconst VARCHAR(255) NOT NULL,
            averageRating FLOAT,
            numVotes INTEGER
        );
    """)

    staging_imdb_title_crew_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_imdb_title_crew (
            tconst VARCHAR(255) NOT NULL,
            directors VARCHAR(255),
            writers VARCHAR(255)    
        );
    """)

    staging_imdb_title_principals_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_imdb_title_principals (
            tconst VARCHAR(255) NOT NULL,
            ordering INTEGER,
            nconst VARCHAR(255),
            category VARCHAR(255),
            job VARCHAR(255),
            characters VARCHAR(255)
        );
    """)

    staging_imdb_name_basics_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_imdb_name_basics (
            nconst VARCHAR(255) NOT NULL,
            primaryName VARCHAR(255),
            birthYear INTEGER,
            deathYear INTEGER,
            primaryProfession VARCHAR(255),
            knownForTitles VARCHAR(255)
        );
    """)

    staging_imdb_title_basics_table_copy = ("""
        COPY staging_imdb_title_basics 
        FROM 's3://udacity-dend/imdb/title.basics.tsv.gz'
        IAM_ROLE '{}'
        REGION 'us-west-2'
        FORMAT AS CSV
        DELIMITER '\t'
        IGNOREHEADER 1
        COMPUPDATE OFF
        STATUPDATE OFF;
    """)


    fact_imdb_title_ratings_table_create = ("""
        CREATE TABLE IF NOT EXISTS fact_imdb_title_ratings (
            title_id VARCHAR(255) NOT NULL PRIMARY KEY,
            average_rating FLOAT,
            num_votes INTEGER
        );
    """)

    dim_imdb_title_basics_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_imdb_title_basics (
            title_id VARCHAR(255) NOT NULL PRIMARY KEY,
            title_type VARCHAR(255),
            primary_title VARCHAR(255),
            original_title VARCHAR(255),
            is_adult INTEGER,
            start_year INTEGER,
            end_year INTEGER,
            runtime_minutes INTEGER,
            genres VARCHAR(255)
        );
    """)

    dim_imdb_title_crew_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_imdb_title_crew (
            title_id VARCHAR(255) NOT NULL PRIMARY KEY,
            directors VARCHAR(255),
            writers VARCHAR(255)
        );
    """)

    dim_imdb_title_principals_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_imdb_title_principals (
            title_id VARCHAR(255) NOT NULL PRIMARY KEY,
            ordering INTEGER,
            name_id VARCHAR(255),
            category VARCHAR(255),
            job VARCHAR(255),
            characters VARCHAR(255)
        );
    """)    

    dim_imdb_name_basics_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_imdb_name_basics (
            name_id VARCHAR(255) NOT NULL PRIMARY KEY,
            primary_name VARCHAR(255),
            birth_year INTEGER,
            death_year INTEGER,
            primary_profession VARCHAR(255),
            known_for_titles VARCHAR(255)
        );
    """)

    fact_imdb_title_ratings_table_insert = ("""
        INSERT INTO fact_imdb_title_ratings (
            title_id,
            average_rating,
            num_votes
        )
        SELECT
            tconst,
            averageRating,
            numVotes
        FROM staging_imdb_title_ratings;
    """)

    dim_imdb_title_basics_table_insert = ("""
        INSERT INTO dim_imdb_title_basics (
            title_id,
            title_type,
            primary_title,
            original_title,
            is_adult,
            start_year,
            end_year,
            runtime_minutes,
            genres
        )
        SELECT
            tconst,
            titleType,
            primaryTitle,
            originalTitle,
            isAdult,
            startYear,
            endYear,
            runtimeMinutes,
            genres
        FROM staging_imdb_title_basics;
    """)

    dim_imdb_title_crew_table_insert = ("""
        INSERT INTO dim_imdb_title_crew (
            title_id,
            directors,
            writers
        )
        SELECT
            tconst,
            directors,
            writers
        FROM staging_imdb_title_crew;
    """)

    dim_imdb_title_principals_table_insert = ("""
        INSERT INTO dim_imdb_title_principals (
            title_id,
            ordering,
            name_id,
            category,
            job,
            characters
        )
        SELECT
            tconst,
            ordering,
            nconst,
            category,
            job,
            characters
        FROM staging_imdb_title_principals;
    """)

    dim_imdb_name_basics_table_insert = ("""
        INSERT INTO dim_imdb_name_basics (
            name_id,
            primary_name,
            birth_year,
            death_year,
            primary_profession,
            known_for_titles
        )
        SELECT
            nconst,
            primaryName,
            birthYear,
            deathYear,
            primaryProfession,
            knownForTitles
        FROM staging_imdb_name_basics;
    """)


