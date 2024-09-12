import sqlite3
from _typeshed import Incomplete
from amsdal_data.connections.enums import ModifyOperation as ModifyOperation
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.implementations.mixins.sql_state_connection_mixin import SqlStateConnectionMixin as SqlStateConnectionMixin
from amsdal_data.connections.state_base import StateConnectionBase as StateConnectionBase
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator as CursorPaginator, NumberPaginator as NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.utils import Q
from pathlib import Path
from typing import Any

logger: Incomplete

class SqliteStateConnection(SqlStateConnectionMixin, StateConnectionBase):
    """
    Manages the SQLite database connection and operations for state management.

    This class provides methods to connect, disconnect, and perform various database operations
    such as insert, update, delete, and query on the SQLite database. It also supports transaction
    management and revert operations.

    Args:
        is_revert_supported (bool): Indicates if revert operations are supported. Defaults to True.
    """
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def is_connected(self) -> bool:
        """
        Checks if the SQLite database connection is established.

        This method returns True if the SQLite database connection is established, otherwise it returns False.

        Returns:
            bool: True if the connection is established, False otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the SQLite database connection is alive.

        This method returns True if the SQLite database connection is alive and can execute a simple query,
        otherwise it returns False. It attempts to execute a simple 'SELECT 1' query to verify the connection.

        Returns:
            bool: True if the connection is alive, False otherwise.
        """
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Provides the table schema manager for the SQLite database.

        This property returns an instance of `SqliteStateTableSchemaService`, which is responsible for managing
        the table schemas in the SQLite database. It is used to resolve table names and perform other schema-related
        operations.

        Returns:
            TableSchemaServiceBase: An instance of `SqliteStateTableSchemaService` for managing table schemas.
        """
    def connect(self, db_path: Path, **kwargs: Any) -> None:
        """
        Connects to the SQLite database.

        This method establishes a connection to the SQLite database at the specified path.
        If the connection is already established, it raises an AmsdalConnectionError.

        Args:
            db_path (Path): The path to the database.
            kwargs (Any): The connection parameters.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is already established.
        """
    def disconnect(self) -> None:
        """
        Disconnects from the SQLite database.

        This method closes the connection to the SQLite database if it is currently established.
        If the connection is not established, it raises an AmsdalConnectionError.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is not established.
        """
    def _add_revert_data(self, operation: ModifyOperation, address: Address, data: dict[str, Any]) -> None: ...
    def insert(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts a data entry into the SQLite database.

        This method inserts the provided data entry into the SQLite database at the specified address.
        If revert is enabled, it adds the data to the revert stack for potential rollback. It resolves the table name,
        maps the fields, and builds the insert statement before executing it.

        Args:
            address (Address): The address where the data will be inserted.
            data (dict[str, Any]): The data to be inserted.

        Returns:
            None
        """
    def bulk_insert(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts multiple data entries into the SQLite database in bulk.

        This method inserts the provided list of data entries into the SQLite database at the specified addresses.
        If revert is enabled, it adds the data to the revert stack for potential rollback. It resolves the table name,
        maps the fields, and builds the bulk insert statement before executing it.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): The list of tuples containing addresses and data to be inserted

        Returns:
            None
        """
    def update(self, address: Address, data: dict[str, Any]) -> None:
        """
        Updates a data entry in the SQLite database.

        This method updates the provided data entry in the SQLite database at the specified address.
        If revert is enabled, it adds the current data to the revert stack for potential rollback.
        It resolves the table name, maps the fields, and builds the update statement before executing it.

        Args:
            address (Address): The address where the data will be updated.
            data (dict[str, Any]): The data to be updated.

        Returns:
            None
        """
    def bulk_update(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Updates multiple data entries in the SQLite database in bulk.

        This method updates the provided list of data entries in the SQLite database at the specified addresses.
        If revert is enabled, it logs a warning that revert is not supported for bulk updates.
        It resolves the table name, maps the fields, and builds the bulk update statement before executing it.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): The list of tuples containing addresses and data to be updated.

        Returns:
            None
        """
    def delete(self, address: Address) -> None:
        """
        Deletes a data entry from the SQLite database.

        This method deletes the data entry in the SQLite database at the specified address.
        If revert is enabled, it adds the current data to the revert stack for potential rollback.
        It resolves the table name, builds the delete statement, and executes it.

        Args:
            address (Address): The address where the data will be deleted.

        Returns:
            None
        """
    def bulk_delete(self, addresses: list[Address]) -> None:
        """
        Deletes multiple data entries from the SQLite database in bulk.

        This method deletes the provided list of data entries from the SQLite database at the specified addresses.
        If revert is enabled, it adds the current data to the revert stack for potential rollback.
        It resolves the table name, maps the fields, and builds the bulk delete statement before executing it.

        Args:
            addresses (list[Address]): The list of addresses where the data will be deleted.

        Returns:
            None
        """
    def begin(self) -> None:
        """
        Begins a new transaction in the SQLite database.

        This method starts a new transaction by appending an empty list to the revert data stack.
        If SQLite does not support nested transactions, it logs a warning and uses the outermost transaction.

        Returns:
            None
        """
    def commit(self) -> None:
        """
        Commits the current transaction in the SQLite database.

        This method commits the current transaction by executing the 'COMMIT' statement if there
            are no nested transactions.
        It also clears the revert operations for the current transaction level.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the changes made in the current transaction.

        This method reverts the changes made in the current transaction by performing the reverse operations
        for each modification recorded in the revert stack. It disables revert support temporarily to avoid
        recursive calls, processes each recorded operation in reverse order, and then re-enables revert support.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If revert is not supported.
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction in the SQLite database.

        This method rolls back the current transaction by executing the 'ROLLBACK' statement if there
            are no nested transactions.
        If there are nested transactions, it reverts the changes made in the current transaction instead.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Queries the SQLite database for data entries matching the specified criteria.

        This method queries the SQLite database for data entries at the specified address that match the given
        query specifier, conditions, pagination, and order by criteria. It resolves the table name, builds the
        select statement, executes the query, and processes the results.

        Args:
            address (Address): The address where the data will be queried.
            query_specifier (QuerySpecifier | None): The query specifier to filter the results. Defaults to None.
            conditions (Q | None): Conditions to filter the results. Defaults to None.
            pagination (NumberPaginator | CursorPaginator | None): Pagination information for the query.
                Defaults to None.
            order_by (list[OrderBy] | None): Order by criteria for the query. Defaults to None.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the queried data entries.
        """
    def _get_record(self, address: Address) -> dict[str, Any]: ...
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        """
        Executes a SQL query on the SQLite database.

        This method executes the provided SQL query with the given arguments on the SQLite database.
        It uses the established connection to create a cursor, execute the query, and return the cursor
        for further processing. If the connection is not established or an error occurs during execution,
        it raises an `AmsdalConnectionError`.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Returns:
            sqlite3.Cursor: The cursor resulting from the executed query.

        Raises:
            AmsdalConnectionError: If the connection is not established or an error occurs during query execution.
        """
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Executes a SQL query on the SQLite database.

        This method executes the provided SQL query with the given arguments on the SQLite database.
        It uses the established connection to create a cursor, execute the query, and return the cursor
        for further processing. If the connection is not established or an error occurs during execution,
        it raises an `AmsdalConnectionError`.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Returns:
            sqlite3.Cursor: The cursor resulting from the executed query.

        Raises:
            AmsdalConnectionError: If the connection is not established or an error occurs during query execution.
        """
    def prepare_connection(self) -> None:
        """
        Prepares the SQLite database connection by registering internal tables.

        This method ensures that the internal tables required for the SQLite database are registered
        and ready for use. It calls the `register_internal_tables` method on the table schema manager.

        Returns:
            None
        """
