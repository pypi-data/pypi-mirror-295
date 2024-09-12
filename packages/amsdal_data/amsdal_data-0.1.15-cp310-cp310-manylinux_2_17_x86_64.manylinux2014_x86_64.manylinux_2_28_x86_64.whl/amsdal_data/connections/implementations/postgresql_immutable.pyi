import psycopg2._psycopg
from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.connections.implementations.mixins.sql_history_conection_mixin import SqlHistoryConnectionMixin as SqlHistoryConnectionMixin
from amsdal_data.connections.implementations.mixins.sqlite_statements_mixin import ADDRESS_FIELD as ADDRESS_FIELD, METADATA_FIELD as METADATA_FIELD, METADATA_TABLE_ALIAS as METADATA_TABLE_ALIAS, MODEL_TABLE_ALIAS as MODEL_TABLE_ALIAS, NoValue as NoValue, SqlOperatorTemplate as SqlOperatorTemplate
from amsdal_data.connections.utils import sort_items as sort_items
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.manager import TableSchemasManager as TableSchemasManager
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q
from typing import Any

logger: Incomplete
METADATA_SELECT_STATEMENT: str
METADATA_SELECT_FIELD: Incomplete
sql_operator_map: dict[Lookup, SqlOperatorTemplate]

class PostgresImmutableConnection(SqlHistoryConnectionMixin, HistoricalConnectionBase):
    """
    A connection class for interacting with a PostgreSQL database in an immutable manner.

    This class extends `SqlHistoryConnectionMixin` and `HistoricalConnectionBase` to provide
    functionalities for querying, inserting, and managing data in a PostgreSQL database.

    Attributes:
        TABLE_SEPARATOR (str): The separator used for table names in SQL statements.
        COLUMN_SEPARATOR (str): The separator used for column names in SQL statements.
        SQL_OPERATOR_MAP (dict): A mapping of lookup types to SQL operator templates.
    """
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    SQL_OPERATOR_MAP = sql_operator_map
    def _fields_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    def _field_reverse_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    def _savepoint_name(self) -> str: ...
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _savepoints: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Returns the table schema manager for the PostgreSQL immutable connection.

        This property provides access to the `PostgresImmutableTableSchemaService` which is responsible
        for managing the table schemas in the PostgreSQL database.

        Returns:
            TableSchemaServiceBase: An instance of `PostgresImmutableTableSchemaService` for managing table schemas.
        """
    def _default_envs(self) -> dict[str, Any]: ...
    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is established.

        This property returns `True` if the connection is established, otherwise `False`.

        Returns:
            bool: `True` if the connection is established, `False` otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is alive.

        This method attempts to execute a simple query to verify if the connection is still active.
        If the query execution fails, it indicates that the connection is not alive.

        Returns:
            bool: `True` if the connection is alive, `False` otherwise.
        """
    def connect(self, dsn: str | None = None, **kwargs: Any) -> None:
        """
        Connects to the PostgreSQL database. Raises an AmsdalConnectionError if the connection is already established.

        Args:
            dsn (str | None): The path to the database.
            kwargs (Any): The connection parameters.

        Returns:
            None
        """
    def disconnect(self) -> None:
        """
        Disconnects from the PostgreSQL database.

        This method closes the connection to the PostgreSQL database if it is currently established.
        If the connection is not established, it raises an AmsdalConnectionError.

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
            Any: The processed value, converted to a JSON string if necessary.
        """
    def begin(self) -> None:
        """
        Begins a new transaction or creates a savepoint if a transaction is already in progress.

        This method starts a new transaction by appending an empty list to the `_revert_data` attribute.
        If there are already transactions in progress, it creates a savepoint to allow partial rollbacks.

        Returns:
            None
        """
    def commit(self) -> None:
        """
        Commits the current transaction or savepoint.

        This method finalizes the current transaction or savepoint by committing all changes made during
            the transaction.
        If there are nested transactions, it commits the current savepoint and retains the outer transactions.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the last transaction.

        This method reverts the last transaction by deleting the data that was added during the transaction.
        If revert is not supported, it raises an AmsdalConnectionError.

        Raises:
            AmsdalConnectionError: If revert is not supported.

        Returns:
            None
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction or savepoint.

        This method reverts the current transaction or savepoint by rolling back all changes made during
            the transaction.
        If there are nested transactions, it rolls back to the current savepoint and retains the outer transactions.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Queries the PostgreSQL database for records matching the specified criteria.

        This method constructs and executes a query to retrieve records from the PostgreSQL database
        based on the provided address, query specifier, conditions, pagination, and order by parameters.

        Args:
            address (Address): The address specifying the target table and object.
            query_specifier (QuerySpecifier | None): The specifier for the query, including fields to select.
            conditions (Q | None): The conditions to filter the query results.
            pagination (NumberPaginator | CursorPaginator | None): The pagination information for the query.
            order_by (list[OrderBy] | None): The list of fields to order the query results by.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the query results.
        """
    @staticmethod
    def _paginate_items(items: list[dict[str, Any]], pagination: NumberPaginator | CursorPaginator | None) -> list[dict[str, Any]]: ...
    def execute(self, query: str, *args: Any) -> psycopg2._psycopg.cursor:
        """
        Executes a SQL query using the established PostgreSQL connection.

        This method executes the provided SQL query with the given arguments using the current
        PostgreSQL connection. If the connection is not established, it raises an AmsdalConnectionError.
        If an error occurs during query execution, it raises an AmsdalConnectionError with the error details.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Raises:
            AmsdalConnectionError: If the connection is not established or if an error occurs during query execution.

        Returns:
            psycopg2._psycopg.cursor: The cursor object after executing the query.
        """
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Counts the number of records in the PostgreSQL database that match the specified criteria.

        This method constructs and executes a query to count the number of records in the PostgreSQL database
        based on the provided address and conditions.

        Args:
            address (Address): The address specifying the target table and object.
            conditions (Q | None): The conditions to filter the count query.

        Returns:
            int: The number of records that match the specified criteria.
        """
    def prepare_connection(self) -> None:
        """
        Prepares the connection by registering internal tables.

        This method ensures that the internal tables required for the PostgreSQL immutable connection
        are registered and available for use.

        Returns:
            None
        """
    def _add_revert_data(self, address: Address, data: dict[str, Any]) -> None: ...
    def _delete(self, address: Address) -> None: ...
    def _nested_filter_statement(self, table_name: str, field_name: str, nested_fields: str, sql_operator_template: SqlOperatorTemplate, value: Any, value_type: Any, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> tuple[str, Any]: ...
    def _resolve_nested_field_name(self, table_name: str, field_name: str, nested_fields: str, *, value_type: Any = ..., is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _select_with_internal_meta_statement(self, table_name: str, select_only: str, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> tuple[str, list[Any]]: ...
    def _build_group_by_statement(self, table_name: str, order_by: list[OrderBy] | None, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _build_select_statement(self, table_name: str, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, *, use_internal_meta_tables: bool = False) -> tuple[str, list[Any]]: ...
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts a record into the PostgreSQL database.

        This method inserts a record into the PostgreSQL database based on the provided address and data.
        If revert is enabled, it adds the data to the revert data list for potential rollback.

        Args:
            address (Address): The address specifying the target table and object.
            data (dict[str, Any]): The data to be inserted into the database.

        Returns:
            None
        """
    def _query(self, table_name: str, query_specifier: QuerySpecifier | None, conditions: Q | None, pagination: NumberPaginator | CursorPaginator | None, order_by: list[OrderBy] | None) -> list[dict[str, Any]]: ...
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts multiple records into the PostgreSQL database in bulk.

        This method inserts multiple records into the PostgreSQL database based on the provided list of address
            and data tuples.
        If revert is enabled, it adds the data to the revert data list for potential rollback.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): A list of tuples where each tuple contains
                an address specifying the target table and object, and a dictionary of data to be inserted into
                the database.

        Returns:
            None
        """
