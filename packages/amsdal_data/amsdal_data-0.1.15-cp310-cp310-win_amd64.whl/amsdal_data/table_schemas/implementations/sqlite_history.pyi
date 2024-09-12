from amsdal_data.connections.implementations.sqlite_state import SqliteStateConnection as SqliteStateConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_data.transactions.constants import TRANSACTION_CLASS_NAME as TRANSACTION_CLASS_NAME
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema
from typing import Any

class SqliteHistoricalTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service for managing historical table schemas in a SQLite database.

    This service provides methods to register, unregister, and update historical table schemas
    in a SQLite database. It also handles the creation of internal tables and their indexes.

    Attributes:
        connection (SqliteStateConnection): The connection to the SQLite database.
    """
    connection: SqliteStateConnection
    def register_table(self, table_schema: TableSchema, *, is_internal_table: bool = False) -> tuple[str, bool]:
        """
        Registers a table in the SQLite database.

        This method checks if a table with the specified schema already exists in the SQLite database.
        If the table does not exist, it creates the table and its indexes. If the table exists, it does nothing.

        Args:
            table_schema (TableSchema): The schema definition for the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating whether the table was created.
        """
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table from the SQLite database.

        This method drops the table corresponding to the provided address from the SQLite database.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name from an address.

        This method converts the class name of the provided address to camel case to form the table name.
        If the class name matches the transaction class name, it returns the class name in lowercase.
        If the class version is the latest, it retrieves the latest class version and appends it to the table name.

        Args:
            address (Address): The address from which to resolve the table name.

        Returns:
            str: The resolved table name.
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_index(self, table_name: str, column_name: str) -> None:
        """
        Creates an index on a specified column in a table.

        This method builds and executes a SQL statement to create an index on the specified column
        in the given table.

        Args:
            table_name (str): The name of the table on which to create the index.
            column_name (str): The name of the column on which to create the index.

        Returns:
            None
        """
    def create_table(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False) -> None:
        """
        Creates a table in the SQLite database.

        This method generates and executes a SQL statement to create a table with the specified schema.
        It can optionally mark the table as an internal table.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema definition for the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            None
        """
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
