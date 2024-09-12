import psycopg2._psycopg
from _typeshed import Incomplete
from amsdal_data.connections.enums import ModifyOperation as ModifyOperation
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.implementations.mixins.sql_state_connection_mixin import SqlStateConnectionMixin as SqlStateConnectionMixin
from amsdal_data.connections.implementations.mixins.sqlite_statements_mixin import ADDRESS_FIELD as ADDRESS_FIELD, METADATA_FIELD as METADATA_FIELD, METADATA_TABLE_ALIAS as METADATA_TABLE_ALIAS, MODEL_TABLE_ALIAS as MODEL_TABLE_ALIAS, NoValue as NoValue, SqlOperatorTemplate as SqlOperatorTemplate
from amsdal_data.connections.state_base import StateConnectionBase as StateConnectionBase
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator as CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q
from typing import Any

logger: Incomplete
METADATA_SELECT_STATEMENT: str
METADATA_SELECT_FIELD: Incomplete
sql_operator_map: dict[Lookup, SqlOperatorTemplate]

class PostgresStateConnection(SqlStateConnectionMixin, StateConnectionBase):
    """
    Represents a connection to a PostgreSQL database with state management capabilities.

    This class provides methods to interact with a PostgreSQL database, including executing queries,
    inserting, updating, and deleting records, as well as managing transactions and revert operations.

    Attributes:
        TABLE_SEPARATOR (str): The character used to separate table names in SQL statements.
        COLUMN_SEPARATOR (str): The character used to separate column names in SQL statements.
        SQL_OPERATOR_MAP (dict): A mapping of lookup operations to their corresponding SQL templates.
        SUBSTITUTE_CHAR (str): The character used as a placeholder for parameter substitution in SQL statements.
    """
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    SQL_OPERATOR_MAP = sql_operator_map
    SUBSTITUTE_CHAR: str
    def _savepoint_name(self) -> str: ...
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _savepoints: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Provides access to the table schema manager for the PostgreSQL state connection.

        This property returns an instance of `TableSchemaServiceBase` that is used to manage
        the table schemas for the PostgreSQL state connection.

        Returns:
            TableSchemaServiceBase: An instance of the table schema manager.
        """
    def _default_envs(self) -> dict[str, Any]: ...
    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is established.

        This method verifies whether the connection to the PostgreSQL database is currently established.

        Returns:
            bool: True if the connection is established, False otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is alive.

        This method verifies whether the connection to the PostgreSQL database is currently alive by executing
            a simple query.

        Returns:
            bool: True if the connection is alive, False otherwise.
        """
    def connect(self, dsn: str | None = None, **kwargs: Any) -> None:
        """
        Connects to the PostgreSQL database.

        This method establishes a connection to the PostgreSQL database using the provided DSN and connection
            parameters.
        Raises an AmsdalConnectionError if the connection is already established.

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
        Raises an AmsdalConnectionError if the connection is not established.

        Returns:
            None
        """
    def _describe_table(self, table_name: str) -> dict[str, str]: ...
    def _build_insert_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_insert_statement(self, table_name: str, data: list[dict[str, Any]]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_delete_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_delete_statement(self, table_name: str, data: list[dict[str, Any]]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_update_statement(self, data: list[tuple[Address, dict[str, Any]]]) -> tuple[str, tuple[Any, ...]]: ...
    def process_value_before_insert(self, value: Any, data_type: str) -> Any: ...
    def _add_revert_data(self, operation: ModifyOperation, address: Address, data: dict[str, Any]) -> None: ...
    def insert(self, address: Address, data: dict[str, Any]) -> None:
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
    def bulk_insert(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
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
    def update(self, address: Address, data: dict[str, Any]) -> None:
        """
        Updates a record in the PostgreSQL database.

        This method updates a record in the PostgreSQL database based on the provided address and data.
        If revert is enabled, it saves the current data for potential rollback.

        Args:
            address (Address): The address specifying the target table and object.
            data (dict[str, Any]): The data to be updated in the database.

        Returns:
            None
        """
    def bulk_update(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Updates multiple records in the PostgreSQL database in bulk.

        This method updates multiple records in the PostgreSQL database based on the provided list of address
            and data tuples.
        If revert is enabled, it logs a warning that revert is not supported for bulk updates.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): A list of tuples where each tuple contains
                an address specifying the target table and object, and a dictionary of data to be updated in
                the database.

        Returns:
            None
        """
    def delete(self, address: Address) -> None:
        """
        Deletes a record from the PostgreSQL database.

        This method deletes a record from the PostgreSQL database based on the provided address.
        If revert is enabled, it saves the current data for potential rollback.

        Args:
            address (Address): The address specifying the target table and object.

        Returns:
            None
        """
    def bulk_delete(self, addresses: list[Address]) -> None:
        """
        Deletes multiple records from the PostgreSQL database in bulk.

        This method deletes multiple records from the PostgreSQL database based on the provided list of addresses.
        If revert is enabled, it saves the current data for potential rollback.

        Args:
            addresses (list[Address]): A list of addresses specifying the target tables and objects to be deleted.

        Returns:
            None
        """
    def begin(self) -> None:
        """
        Begins a new transaction or savepoint.

        This method starts a new transaction if no transactions are currently active.
        If a transaction is already active, it creates a new savepoint for nested transactions.
        It also initializes a list to store revert data for potential rollback.

        Returns:
            None
        """
    def commit(self) -> None:
        """
        Commits the current transaction or savepoint.

        This method commits the current transaction if no savepoints are active.
        If savepoints are active, it commits the current savepoint and merges its revert operations
        with the previous savepoint or transaction.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the changes made in the current transaction.

        This method reverts the changes made in the current transaction by performing the opposite operations
        (delete, update, insert) in reverse order. If revert is not supported, it raises an AmsdalConnectionError.

        Raises:
            AmsdalConnectionError: If revert is not supported.

        Returns:
            None
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction or savepoint.

        This method rolls back the current transaction if no savepoints are active.
        If savepoints are active, it rolls back to the most recent savepoint and removes it from the savepoints list.
        It also removes the revert data for the current transaction or savepoint.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Executes a query on the PostgreSQL database.

        This method executes a query on the PostgreSQL database based on the provided address, query specifier,
            conditions, pagination, and order by parameters. It returns a list of dictionaries representing
            the query results.

        Args:
            address (Address): The address specifying the target table and object.
            query_specifier (QuerySpecifier | None): An optional query specifier to refine the query.
            conditions (Q | None): Optional conditions to filter the query results.
            pagination (NumberPaginator | CursorPaginator | None): Optional pagination parameters to limit
                the query results.
            order_by (list[OrderBy] | None): Optional order by parameters to sort the query results.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the query results.
        """
    def _get_record(self, address: Address) -> dict[str, Any]: ...
    def execute(self, query: str, *args: Any) -> psycopg2._psycopg.cursor:
        """
        Executes a SQL query on the PostgreSQL database.

        This method executes a SQL query on the PostgreSQL database using the provided query string and arguments.
        It returns a cursor object that can be used to fetch the results of the query.
        If the connection is not established, it raises an AmsdalConnectionError.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Returns:
            psycopg2._psycopg.cursor: A cursor object to fetch the results of the query.

        Raises:
            AmsdalConnectionError: If the connection is not established or if there is an error executing the query.
        """
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Counts the number of records in the PostgreSQL database.

        This method counts the number of records in the PostgreSQL database based on the provided address
            and optional conditions.
        It returns the count of records that match the specified conditions.

        Args:
            address (Address): The address specifying the target table and object.
            conditions (Q | None): Optional conditions to filter the records to be counted.

        Returns:
            int: The count of records that match the specified conditions.
        """
    def prepare_connection(self) -> None:
        """
        Prepares the connection to the PostgreSQL database.

        This method is intended to perform any necessary preparations or initializations
        required before establishing a connection to the PostgreSQL database.

        Returns:
            None
        """
    def _select_statement(self, table_name: str, select_only: str, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, *, is_internal_table: bool = False) -> tuple[str, list[Any]]: ...
    def _resolve_nested_field_name(self, table_name: str, field_name: str, nested_fields: str, *, value_type: Any = ..., is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _nested_filter_statement(self, table_name: str, field_name: str, nested_fields: str, sql_operator_template: SqlOperatorTemplate, value: Any, value_type: Any, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> tuple[str, Any]: ...
