import psycopg2._psycopg
from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.connections.implementations.mixins.sql_history_conection_mixin import SqlHistoryConnectionMixin as SqlHistoryConnectionMixin
from amsdal_data.connections.implementations.mixins.sqlite_statements_mixin import ADDRESS_FIELD as ADDRESS_FIELD, METADATA_FIELD as METADATA_FIELD, METADATA_TABLE_ALIAS as METADATA_TABLE_ALIAS, MODEL_TABLE_ALIAS as MODEL_TABLE_ALIAS, NoValue as NoValue, SqlOperatorTemplate as SqlOperatorTemplate
from amsdal_data.connections.utils import sort_items as sort_items
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q as Q
from typing import Any

logger: Incomplete
METADATA_SELECT_STATEMENT: str
METADATA_SELECT_FIELD: Incomplete
sql_operator_map: dict[Lookup, SqlOperatorTemplate]

class PostgresHistoricalConnection(SqlHistoryConnectionMixin, HistoricalConnectionBase):
    """
    A class to manage historical connections to a PostgreSQL database.

    Attributes:
        TABLE_SEPARATOR (str): The separator used for table names in SQL queries.
        COLUMN_SEPARATOR (str): The separator used for column names in SQL queries.
        SQL_OPERATOR_MAP (dict): A mapping of lookup types to SQL operator templates.
    """
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    SQL_OPERATOR_MAP = sql_operator_map
    def _savepoint_name(self) -> str: ...
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _savepoints: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Returns the table schema manager for the PostgreSQL historical connection.

        This property dynamically imports and returns the `PostgresHistoricalTableSchemaService` class,
        which is responsible for managing the table schema for historical data in PostgreSQL.

        Returns:
            TableSchemaServiceBase: An instance of `PostgresHistoricalTableSchemaService` for managing table schemas.
        """
    def _default_envs(self) -> dict[str, Any]: ...
    def connect(self, dsn: str | None = None, **kwargs: Any) -> None:
        """
        Connects to the PostgreSQL database.

        Raises:
            AmsdalConnectionError: If the connection is already established.

        Args:
            dsn (str | None): The path to the database.
            kwargs (Any): The connection parameters.

        Returns:
            None
        """
    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is established.

        Returns:
            bool: True if the connection is established, False otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is alive.

        Returns:
            bool: True if the connection is alive, False otherwise.
        """
    def disconnect(self) -> None:
        """
        Disconnects from the PostgreSQL database.

        Raises:
            AmsdalConnectionError: If the connection is not established.

        Returns:
            None
        """
    def _describe_table(self, table_name: str) -> dict[str, str]: ...
    def _build_insert_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_insert_statement(self, table_name: str, data: list[dict[str, Any]]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_delete_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def process_value_before_insert(self, value: Any, data_type: str) -> Any:
        """
        Processes the value before inserting it into the PostgreSQL database.

        This method converts the value to a JSON string if the data type is 'json' and the value is a string or integer.

        Args:
            value (Any): The value to be processed.
            data_type (str): The data type of the value.

        Returns:
            Any: The processed value, which may be converted to a JSON string if the data type is 'json'.
        """
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts data into the PostgreSQL database for the given address.

        If revert is enabled, the data is added to the revert data list for potential rollback.

        Args:
            address (Address): The address object containing the object ID and version.
            data (dict[str, Any]): The data to be inserted into the database.

        Returns:
            None
        """
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts multiple records into the PostgreSQL database.

        If revert is enabled, the data is added to the revert data list for potential rollback.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): A list of tuples where each tuple contains an Address object
                and a dictionary of data to be inserted.

        Returns:
            None
        """
    def begin(self) -> None:
        """
        Begins a new transaction.

        If there are already active transactions, a savepoint is created to allow partial rollbacks.

        Returns:
            None
        """
    def commit(self) -> None:
        """
        Commits the current transaction.

        If there are active savepoints, the savepoint is released. Otherwise, the transaction is committed.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the last set of changes made during the current transaction.

        This method removes the last set of changes from the revert data list and deletes the corresponding records
        from the PostgreSQL database. If revert is not supported, an `AmsdalConnectionError` is raised.

        Raises:
            AmsdalConnectionError: If revert is not supported.

        Returns:
            None
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction.

        If there are active savepoints, the transaction is rolled back to the most recent savepoint.
        Otherwise, the entire transaction is rolled back.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Queries the PostgreSQL database for records matching the specified criteria.

        Args:
            address (Address): The address object containing the object ID and version.
            query_specifier (QuerySpecifier | None): Specifies the fields to include in the query results.
            conditions (Q | None): The conditions to filter the query results.
            pagination (NumberPaginator | CursorPaginator | None): The pagination object to limit the query results.
            order_by (list[OrderBy] | None): The list of fields to order the query results.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the query results.
        """
    @staticmethod
    def _paginate_items(items: list[dict[str, Any]], pagination: NumberPaginator | CursorPaginator | None) -> list[dict[str, Any]]: ...
    def execute(self, query: str, *args: Any) -> psycopg2._psycopg.cursor:
        """
        Executes a SQL query on the PostgreSQL database.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Raises:
            AmsdalConnectionError: If the connection is not established or if there is an error executing the query.

        Returns:
            psycopg2._psycopg.cursor: The cursor object after executing the query.
        """
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Counts the number of records in the PostgreSQL database that match the specified criteria.

        Args:
            address (Address): The address object containing the object ID and version.
            conditions (Q | None): The conditions to filter the records.

        Returns:
            int: The number of records that match the specified criteria.
        """
    def prepare_connection(self) -> None:
        """
        Prepares the connection by registering internal tables with the table schema manager.

        This method ensures that the necessary internal tables are registered before performing any database operations.

        Returns:
            None
        """
    def _add_revert_data(self, address: Address, data: dict[str, Any]) -> None: ...
    def _delete(self, address: Address) -> None: ...
    def _query(self, table_name: str, query_specifier: QuerySpecifier | None, conditions: Q | None, pagination: NumberPaginator | CursorPaginator | None, order_by: list[OrderBy] | None) -> list[dict[str, Any]]: ...
    def _nested_filter_statement(self, table_name: str, field_name: str, nested_fields: str, sql_operator_template: SqlOperatorTemplate, value: Any, value_type: Any, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> tuple[str, Any]: ...
    def _resolve_nested_field_name(self, table_name: str, field_name: str, nested_fields: str, *, value_type: Any = ..., is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _select_with_internal_meta_statement(self, table_name: str, select_only: str, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> tuple[str, list[Any]]: ...
    def _build_group_by_statement(self, table_name: str, order_by: list[OrderBy] | None, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _build_select_statement(self, table_name: str, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, *, use_internal_meta_tables: bool = False) -> tuple[str, list[Any]]: ...
