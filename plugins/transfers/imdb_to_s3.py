from airflow.models import BaseOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class ImdbToS3Operator(BaseOperator):
    """
    Operator to transfer data from IMDB to S3.
    """

    def __init__(
            self,
            *,
            key,
            bucket_name,
            endpoint="title.basics.tsv.gz",
            replace=True,
            acl_policy=None,
            imdb_conn_id="imdb_default",
            s3_conn_id="s3_default",
            **kwargs
            ):
        
        super().__init__(**kwargs)

        self.key = key
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.replace = replace
        self.acl_policy = acl_policy
        self.imdb_conn_id = imdb_conn_id
        self.s3_conn_id = s3_conn_id


    def execute(self, context):
        """
        Executes the operator.
        """

        imdb_hook = HttpHook(
            method="GET",
            http_conn_id=self.imdb_conn_id,
            )
        
        s3_hook = S3Hook(
            aws_conn_id=self.s3_conn_id
            )

        # Get the pushshift data
        response = imdb_hook.run(
            endpoint=self.endpoint,
        )

        # Upload the data to S3
        s3_hook.load_bytes(
            bytes_data=response.content,
            key=self.key,
            bucket_name=self.bucket_name,
            replace=self.replace,
            acl_policy=self.acl_policy,
        )

