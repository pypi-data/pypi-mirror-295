from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.implementations.sqlite_immutable import SqliteImmutableConnection as SqliteImmutableConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_data.transactions.constants import TRANSACTION_CLASS_NAME as TRANSACTION_CLASS_NAME
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema
from typing import Any

class SqliteImmutablelTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service class for managing SQLite immutable table schemas.

    This class provides methods to register, unregister, and update table schemas in an SQLite database.
    It also includes functionality to create and manage internal tables and indexes.

    Attributes:
        connection (SqliteImmutableConnection): The SQLite connection used for executing SQL statements.
    """
    connection: SqliteImmutableConnection
    def register_table(self, table_schema: TableSchema, *, is_internal_table: bool = False) -> tuple[str, bool]:
        """
        Registers a table in the SQLite database.

        This method checks if a table with the specified schema already exists in the database.
        If the table exists, it updates the table schema. If the table does not exist, it creates a new table.
        It also creates indexes for the table based on the schema.

        Args:
            table_schema (TableSchema): The schema definition for the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating whether the table was created.
        """
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table from the SQLite database.

        This method drops the table corresponding to the given address from the SQLite database.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name from the given address.

        This method converts the class name from the address to a lowercase string to be used as the table name.

        Args:
            address (Address): The address object containing the class name.

        Returns:
            str: The resolved table name in lowercase.
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_index(self, table_name: str, column_name: str) -> None:
        """
        Creates an index on a specified column in a table.

        This method generates and executes an SQL statement to create an index on the specified column
        in the given table. If an error occurs during the execution, it is caught and ignored.

        Args:
            table_name (str): The name of the table on which to create the index.
            column_name (str): The name of the column on which to create the index.

        Returns:
            None
        """
    def create_table(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False) -> None:
        """
        Creates a table in the SQLite database.

        This method generates and executes an SQL statement to create a table with the specified schema
        in the SQLite database. It also handles the creation of internal and historical tables.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema definition for the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def update_table(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn], *, is_internal_table: bool = False) -> None:
        """
        Updates the schema of a table in the SQLite database.

        This method generates and executes SQL statements to update the schema of a table
        to match the provided table schema. It adds new columns and modifies existing columns as needed.

        Args:
            table_name (str): The name of the table to update.
            table_schema (TableSchema): The new schema definition for the table.
            table_columns (list[SqlTableColumn]): The current columns of the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def _build_columns_from_schema(self, table_schema: TableSchema, *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[SqlTableColumn]: ...
    def _build_update_table_statements(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn], *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[str]: ...
    def register_internal_tables(self) -> None:
        """
        Registers internal tables in the SQLite database.

        This method registers a set of predefined internal tables in the SQLite database.
        If a table already exists, it updates the table schema to match the predefined schema.

        Returns:
            None
        """
    def update_internal_table(self, table_schema: TableSchema) -> None:
        """
        Updates the schema of an internal table in the SQLite database.

        This method generates and executes SQL statements to update the schema of an internal table
        to match the provided table schema. It adds new columns and modifies existing columns as needed.

        Args:
            table_schema (TableSchema): The new schema definition for the internal table.

        Returns:
            None
        """
