import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from transfers.imdb_to_s3 import ImdbToS3Operator
from helpers.sql_queries import SqlQueries
from operators.data_quality import DataQualityOperator
from operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

default_args = {
    "owner": "udacity",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_retry": False,
    "catchup": False,
}


with DAG(
    dag_id="etl_imdb",
    default_args=default_args,
    description="Load and transform data in Redshift with Airflow",
    schedule_interval="@daily",
    tags=["udacity", "imdb", "etl"],
) as dag:
    start_operator = DummyOperator(task_id="Start")

    with TaskGroup("Fetch_Data") as fetch_data:
        fetch_imdb_data = ImdbToS3Operator(
            task_id="Fetch_IMDB_Data",
            key="imdb/title.basics.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.basics.tsv.gz",
            replace=True,
        )

        fetch_imdb_ratings = ImdbToS3Operator(
            task_id="Fetch_IMDB_Ratings",
            key="imdb/title.ratings.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.ratings.tsv.gz",
            replace=True,
        )

        fetch_imdb_crew = ImdbToS3Operator(
            task_id="Fetch_IMDB_Crew",
            key="imdb/title.crew.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.crew.tsv.gz",
            replace=True,
        )

        fetch_imdb_principals = ImdbToS3Operator(
            task_id="Fetch_IMDB_Principals",
            key="imdb/title.principals.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.principals.tsv.gz",
            replace=True,
        )

        fetch_imdb_names = ImdbToS3Operator(
            task_id="Fetch_IMDB_Names",
            key="imdb/name.basics.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="name.basics.tsv.gz",
            replace=True,
        )

        fetch_imdb_akas = ImdbToS3Operator(
            task_id="Fetch_IMDB_Akas",
            key="imdb/title.akas.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.akas.tsv.gz",
            replace=True,
        )

        fetch_imdb_episode = ImdbToS3Operator(
            task_id="Fetch_IMDB_Episode",
            key="imdb/title.episode.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.episode.tsv.gz",
            replace=True,
        )


    with TaskGroup("Create_Tables") as create_tables:
        create_imdb_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_basics_create,
        )

        create_imdb_ratings_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Ratings_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_ratings_create,
        )

        create_imdb_crew_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Crew_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_crew_create,
        )

        create_imdb_principals_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Principals_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_principals_create,
        )

        create_imdb_names_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Names_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_name_basics_create,
        )

        create_imdb_akas_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Akas_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_akas_create,
        )

        create_imdb_episode_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Episode_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_episode_create,
        )

    with TaskGroup("Load_Data") as load_data:
        load_data_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Data_to_Redshift",
            schema="public",
            table="imdb_title_basics",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.basics.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_ratings_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Ratings_to_Redshift",
            schema="public",
            table="imdb_title_ratings",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.ratings.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_crew_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Crew_to_Redshift",
            schema="public",
            table="imdb_title_crew",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.crew.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_principals_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Principals_to_Redshift",
            schema="public",
            table="imdb_title_principals",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.principals.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_names_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Names_to_Redshift",
            schema="public",
            table="imdb_name_basics",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/name.basics.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_akas_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Akas_to_Redshift",
            schema="public",
            table="imdb_title_akas",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.akas.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

        load_episode_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Episode_to_Redshift",
            schema="public",
            table="imdb_title_episode",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.episode.tsv.gz",
            copy_options=[
                "COMPUPDATE OFF",
                "STATUPDATE OFF",
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "FORMAT AS CSV",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
        )

    with TaskGroup("Data_Quality") as data_quality:
        check_imdb = DataQualityOperator(
            task_id="Check_IMDB",
            redshift_conn_id="redshift",
            tables=["imdb", "imdb_ratings", "imdb_crew", "imdb_principals", "imdb_names", "imdb_akas", "imdb_episode"],
        )


    end_operator = DummyOperator(task_id="End")

    start_operator >> fetch_data >> create_tables >> load_data >> data_quality >> end_operator
