import sqlite3
from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.connections.implementations.mixins.sql_history_conection_mixin import SqlHistoryConnectionMixin as SqlHistoryConnectionMixin
from amsdal_data.connections.utils import sort_items as sort_items
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.manager import TableSchemasManager as TableSchemasManager
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.utils import Q
from pathlib import Path
from typing import Any

logger: Incomplete

class SqliteImmutableConnection(SqlHistoryConnectionMixin, HistoricalConnectionBase):
    """
    Manages an immutable connection to an SQLite database with historical data support.

    This class provides methods to connect to an SQLite database, execute queries, manage transactions,
    and handle historical data. It extends the functionality of `SqlHistoryConnectionMixin` and
    `HistoricalConnectionBase` to support immutable data operations.

    Attributes:
        TABLE_SEPARATOR (str): The separator used for table names.
        COLUMN_SEPARATOR (str): The separator used for column names.
    """
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    def _fields_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    def _field_reverse_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    _is_revert_enabled: Incomplete
    _revert_data: Incomplete
    _connection: Incomplete
    def __init__(self, *, is_revert_supported: bool = True) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Provides access to the table schema manager for the SQLite database.

        This property returns an instance of `SqliteImmutablelTableSchemaService`, which is responsible for
        managing the table schemas in the SQLite database. It ensures that the correct schema service is
        used for the immutable connection.

        Returns:
            TableSchemaServiceBase: The table schema manager for the SQLite database.
        """
    @property
    def is_connected(self) -> bool:
        """
        Checks if the SQLite database connection is established.

        This method verifies whether the connection to the SQLite database is currently established.

        Returns:
            bool: True if the connection is established, False otherwise.
        """
    @property
    def is_alive(self) -> bool:
        """
        Checks if the SQLite database connection is alive.

        This method verifies whether the connection to the SQLite database is currently alive by executing a simple
        query. If the query executes without errors, the connection is considered alive.

        Returns:
            bool: True if the connection is alive, False otherwise.
        """
    def connect(self, db_path: Path, **kwargs: Any) -> None:
        """
        Connects to the SQLite database.

        This method establishes a connection to the SQLite database using the provided database path
            and connection parameters.
        It raises an AmsdalConnectionError if the connection is already established.

        Args:
            db_path (Path): The path to the database.
            **kwargs (Any): The connection parameters.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is already established.
        """
    def disconnect(self) -> None:
        """
        Disconnects from the SQLite database.

        This method closes the connection to the SQLite database if it is currently established.
        It raises an AmsdalConnectionError if the connection is not established.

        Returns:
            None

        Raises:
            AmsdalConnectionError: If the connection is not established.
        """
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts data into the SQLite database.

        This method inserts the provided data into the SQLite database at the specified address.
        If revert is enabled, it adds the data to the revert stack for potential rollback.
        It resolves the table name and maps the fields before executing the insert statement.

        Args:
            address (Address): The address where the data should be inserted.
            data (dict[str, Any]): The data to be inserted.

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

        This method commits the current transaction by executing the `COMMIT` statement if there
            are no nested transactions.
        It also extends the revert data stack with the current revert operations if nested transactions are present.

        Returns:
            None
        """
    def revert(self) -> None:
        """
        Reverts the last transaction in the SQLite database.

        This method reverts the last transaction by deleting the data entries that were added during the transaction.
        It raises an AmsdalConnectionError if revert is not supported.

        Raises:
            AmsdalConnectionError: If revert is not supported.
        """
    def rollback(self) -> None:
        """
        Rolls back the current transaction in the SQLite database.

        This method rolls back the current transaction by executing the `ROLLBACK` statement if there
            are no nested transactions.
        If nested transactions are present, it reverts the last transaction instead.

        Returns:
            None
        """
    def on_transaction_complete(self) -> None:
        """Transaction is completed successfully. Clear the revert data."""
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None) -> list[dict[str, Any]]:
        """
        Queries the SQLite database for entries matching the specified criteria.

        This method queries the SQLite database for data entries that match the specified address,
        query specifier, conditions, pagination, and order by criteria. It builds and executes the
        appropriate SQL select queries and returns the results.

        Args:
            address (Address): The address to query entries for.
            query_specifier (QuerySpecifier | None): The query specifier to refine the query.
            conditions (Q | None): Conditions to filter the query.
            pagination (NumberPaginator | CursorPaginator | None): Pagination information for the query.
            order_by (list[OrderBy] | None): Order by criteria for the query.

        Returns:
            list[dict[str, Any]]: The list of entries matching the specified criteria.
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
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
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
