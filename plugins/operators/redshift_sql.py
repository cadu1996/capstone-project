from typing import TYPE_CHECKING, Iterable, Optional, Sequence, Union

from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.www import utils as wwwutils

if TYPE_CHECKING:
    from airflow.utils.context import Context


class RedshiftSQLOperator(BaseOperator):
    """
    Executes SQL Statements against an Amazon Redshift cluster.

    .. seealso::
        For more information on how to use this operator, take a look at the
        guide:
        :ref:`howto/operator:RedshiftSQLOperator`

    Args:
        sql: The SQL code to be executed as a single string, a list of strings
            (SQL statements), or a reference to a template file. Template
            references are recognized by strings ending in '.sql'.
        redshift_conn_id: Reference to the
            :ref:`Amazon Redshift connection id<howto/connection:redshift>`.
            Default is "redshift_default".
        parameters: (Optional) The parameters to render the SQL query with.
        autocommit: If True, each command is automatically committed.
            Default value is False.
    """

    template_fields: Sequence[str] = ("sql",)

    template_ext: Sequence[str] = (".sql",)

    template_fields_renderers = {
        "sql": "postgresql" if "postgresql" in wwwutils.get_attr_renderer() else "sql"
    }

    def __init__(
        self,
        *,
        sql: Union[str, Iterable[str]],
        redshift_conn_id: str = "redshift_default",
        parameters: Optional[dict] = None,
        autocommit: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.autocommit = autocommit
        self.parameters = parameters

    def get_hook(self) -> RedshiftSQLHook:
        """Create and return a RedshiftSQLHook instance.

        Returns:
            RedshiftSQLHook: A RedshiftSQLHook instance.
        """
        return RedshiftSQLHook(redshift_conn_id=self.redshift_conn_id)

    def execute(self, context: "Context") -> None:
        """Execute a statement against Amazon Redshift."""
        self.log.info("Executing statement: %s", self.sql)
        hook = self.get_hook()
        hook.run(
            self.sql,
            autocommit=self.autocommit,
            parameters=self.parameters
            )
