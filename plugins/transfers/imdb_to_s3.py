from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.hooks.http import HttpHook


class ImdbToS3Operator(BaseOperator):
    """
    Operator to transfer data from IMDB to S3.

    Args:
        key: The key to use for the object in the S3 bucket.
        bucket_name: The name of the S3 bucket.
        endpoint: The IMDB data file to download. Default is
          "title.basics.tsv.gz".
        replace: If True, replace the file in S3 if it exists. Default is True.
        imdb_conn_id: The connection ID to use for IMDB. Default is
          "imdb_default".
        s3_conn_id: The connection ID to use for S3. Default is "s3_default".
    """

    def __init__(
        self,
        *,
        key,
        bucket_name,
        endpoint="title.basics.tsv.gz",
        replace=True,
        imdb_conn_id="imdb_default",
        s3_conn_id="s3_default",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.key = key
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.replace = replace
        self.imdb_conn_id = imdb_conn_id
        self.s3_conn_id = s3_conn_id

    def execute(self, context):
        """
        Executes the operator, downloading data from IMDB and uploading it to
        S3.
        """

        imdb_hook = HttpHook(
            method="GET",
            http_conn_id=self.imdb_conn_id,
        )

        s3_hook = S3Hook(aws_conn_id=self.s3_conn_id)

        response = imdb_hook.run(
            endpoint=self.endpoint,
        )

        s3_hook.load_bytes(
            bytes_data=response.content,
            key=self.key,
            bucket_name=self.bucket_name,
            replace=self.replace,
        )
