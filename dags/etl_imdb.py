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
            s3_conn_id="aws_credentials",
        )

        fetch_imdb_ratings = ImdbToS3Operator(
            task_id="Fetch_IMDB_Ratings",
            key="imdb/title.ratings.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.ratings.tsv.gz",
            replace=True,
            s3_conn_id="aws_credentials",
        )

        fetch_imdb_episode = ImdbToS3Operator(
            task_id="Fetch_IMDB_Episode",
            key="imdb/title.episode.tsv.gz",
            bucket_name="imdb-dend-analytics",
            endpoint="title.episode.tsv.gz",
            replace=True,
            s3_conn_id="aws_credentials",
        )


    with TaskGroup("Create_Tables") as create_tables:
        create_imdb_title_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Title_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_basics_create,
        )

        create_imdb_ratings_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Ratings_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_ratings_create,
        )

        create_imdb_episode_table = RedshiftSQLOperator(
            task_id="Create_IMDB_Episode_Table",
            redshift_conn_id="redshift",
            sql=SqlQueries.imdb_title_episode_create,
        )

    with TaskGroup("stage_data") as stage_data:
        title_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Title_to_Redshift",
            schema="public",
            table="imdb_title_basics",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.basics.tsv.gz",
            copy_options=[
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
            method="REPLACE",
        )

        ratings_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Ratings_to_Redshift",
            schema="public",
            table="imdb_title_ratings",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.ratings.tsv.gz",
            copy_options=[
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
            method="REPLACE",
        )

        episode_to_redshift = S3ToRedshiftOperator(
            task_id="Load_Episode_to_Redshift",
            schema="public",
            table="imdb_title_episode",
            s3_bucket="imdb-dend-analytics",
            s3_key="imdb/title.episode.tsv.gz",
            copy_options=[
                "IGNOREHEADER 1",
                "DELIMITER '\t'",
                "GZIP",
            ],
            redshift_conn_id="redshift",
            aws_conn_id="aws_credentials",
            autocommit=True,
            method="REPLACE",
        )

    with TaskGroup("Data_Quality") as data_quality:
        check_imdb = DataQualityOperator(
            task_id="Check_IMDB",
            redshift_conn_id="redshift",
            tables=["imdb_title_basics", "imdb_title_ratings", "imdb_title_episode"],
        )


    end_operator = DummyOperator(task_id="End")

    start_operator >> fetch_data >> create_tables >> stage_data >> data_quality >> end_operator
