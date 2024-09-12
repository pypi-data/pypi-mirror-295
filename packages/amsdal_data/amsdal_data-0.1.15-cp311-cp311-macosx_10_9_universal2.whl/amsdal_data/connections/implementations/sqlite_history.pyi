import sqlite3
from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.connections.implementations.mixins.sql_history_conection_mixin import SqlHistoryConnectionMixin as SqlHistoryConnectionMixin
from amsdal_data.connections.utils import sort_items as sort_items
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.utils import Q as Q
from pathlib import Path
from typing import Any

logger: Incomplete

class SqliteHistoricalConnection(SqlHistoryConnectionMixin, HistoricalConnectionBase):
    """
    Manages a historical connection to an SQLite database.

    This class provides methods to connect to an SQLite database, execute queries, manage transactions,
    and handle historical data with support for revert operations.
    """
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Returns the table schema manager for the SQLite database.

        This method returns an instance of `SqliteHistoricalTableSchemaService` which is responsible for managing
        the table schemas in the SQLite database.

        Returns:
            TableSchemaServiceBase: An instance of `SqliteHistoricalTableSchemaService` for managing table schemas.
        """
    def connect(self, db_path: Path, **kwargs: Any) -> None:
        """
        Connects to the SQLite database.

        This method establishes a connection to the SQLite database using the provided database path
            and connection parameters.
        If the connection is already established, it raises an AmsdalConnectionError.

        Args:
            db_path (Path): The path to the database.
            **kwargs (Any): The connection parameters.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is already established.
        """
    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the SQLite database is established.

        This method returns a boolean indicating whether the connection to the SQLite database
        has been established.

        Returns:
            bool: True if the connection is established, False otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the connection to the SQLite database is alive.

        This method attempts to execute a simple query on the SQLite database to determine if the connection
        is still active. If the query executes successfully, the connection is considered alive.

        Returns:
            bool: True if the connection is alive, False otherwise.
        """
    def disconnect(self) -> None:
        """
        Disconnects from the SQLite database.

        This method closes the connection to the SQLite database if it is established.
        If the connection is not established, it raises an AmsdalConnectionError.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is not established.
        """
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts data into the SQLite database.

        This method inserts the provided data into the SQLite database at the specified address.
        If revert is enabled, it also stores the data for potential revert operations.

        Args:
            address (Address): The address where the data should be inserted.
            data (dict[str, Any]): The data to be inserted.

        Returns:
            None
        """
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts multiple data entries into the SQLite database.

        This method inserts the provided list of data entries into the SQLite database. Each entry consists of
            an address and the corresponding data to be inserted. If revert is enabled, it also stores
            the data for potential revert operations.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): A list of tuples where each tuple contains an address
                and the data to be inserted.

        Returns:
            None
        """
    def begin(self) -> None:
        """
        Begins a transaction in the SQLite database.

        This method starts a new transaction in the SQLite database. If revert is enabled, it also
        initializes a new list to store revert data. SQLite does not support nested transactions,
        so if a transaction is already in progress, it will use the outermost transaction.

        Returns:
            None
        """
    def commit(self) -> None:
        """
        Commits the current transaction in the SQLite database.

        This method commits the current transaction in the SQLite database. If revert operations are enabled,
        it clears the revert data. SQLite does not support nested transactions, so it only commits if it is
        at the top level of the transaction stack.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the last transaction in the SQLite database.

        This method reverts the last transaction by deleting the data that was inserted during the transaction.
        If revert operations are not supported, it raises an AmsdalConnectionError.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If revert operations are not supported.
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction in the SQLite database.

        This method rolls back the current transaction in the SQLite database. If revert operations are enabled,
        it reverts the data changes. SQLite does not support nested transactions, so it only rolls back if it is
        at the top level of the transaction stack.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Queries the SQLite database for data matching the specified criteria.

        This method queries the SQLite database for data entries that match the specified address, conditions,
        pagination, and order by criteria. It builds and executes the appropriate SQL queries and returns the
        results as a list of dictionaries.

        Args:
            address (Address): The address to query.
            query_specifier (QuerySpecifier | None): Additional query specifications.
            conditions (Q | None): Conditions to filter the query.
            pagination (NumberPaginator | CursorPaginator | None): Pagination information.
            order_by (list[OrderBy] | None): Order by criteria.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the query results.
        """
    @staticmethod
    def _paginate_items(items: list[dict[str, Any]], pagination: NumberPaginator | CursorPaginator | None) -> list[dict[str, Any]]: ...
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        """
        Executes a SQL query on the SQLite database.

        This method executes the provided SQL query on the SQLite database using the established connection.
        It raises an AmsdalConnectionError if the connection is not established or if there is an error
        executing the query.

        Args:
            query (str): The SQL query to be executed.
            *args (Any): The arguments to be passed to the SQL query.

        Returns:
            sqlite3.Cursor: The cursor object containing the results of the query.

        Raises:
            AmsdalConnectionError: If the connection is not established or if there is an error executing the query.
        """
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Counts the number of entries in the SQLite database matching the specified criteria.

        This method counts the number of data entries in the SQLite database that match the specified address
        and conditions. It builds and executes the appropriate SQL count queries and returns the total count.

        Args:
            address (Address): The address to count entries for.
            conditions (Q | None): Conditions to filter the count query.

        Returns:
            int: The total number of entries matching the specified criteria.
        """
    def prepare_connection(self) -> None:
        """
        Prepares the SQLite database connection by registering internal tables.

        This method ensures that the internal tables required for the SQLite database are registered
        and ready for use. It calls the `register_internal_tables` method on the table schema manager.

        Returns:
            None
        """
    def _add_revert_data(self, address: Address, data: dict[str, Any]) -> None: ...
    def _delete(self, address: Address) -> None: ...
    def _query(self, table_name: str, query_specifier: QuerySpecifier | None, conditions: Q | None, pagination: NumberPaginator | CursorPaginator | None, order_by: list[OrderBy] | None) -> list[dict[str, Any]]: ...
