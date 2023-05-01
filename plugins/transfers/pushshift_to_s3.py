from airflow.models import BaseOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class PushshiftToS3Operator(BaseOperator):
    """
    Operator to transfer data from Pushshift to S3.
    """
    def __init__(
            self,
            *,
            key,
            bucket_name,
            params=None,
            endpoint="reddit/submission/search",
            replace=False,
            compression="gzip",
            pushshift_conn_id="pushshift_default",
            s3_conn_id="s3_default",
            **kwargs
            ):
        
        super().__init__(*args, **kwargs)

        self.key = key
        self.bucket_name = bucket_name
        self.params = params
        self.endpoint = endpoint
        self.replace = replace
        self.compression = compression
        self.pushshift_conn_id = pushshift_conn_id
        self.s3_conn_id = s3_conn_id

    def execute(self, context):
        """
        Executes the operator.
        """

        pushshift_hook = HttpHook(
            method="GET",
            http_conn_id=self.pushshift_conn_id,
            )
        
        s3_hook = S3Hook(
            aws_conn_id=self.s3_conn_id
            )

        # Get the pushshift data
        response = pushshift_hook.run(
            endpoint=self.endpoint,
            data=self.params,
        )

        # Upload the data to S3
        s3_hook.load_string(
            string_data=response.text,
            key=self.key,
            bucket_name=self.bucket_name,
            replace=self.replace,
            compression=self.compression,
        )