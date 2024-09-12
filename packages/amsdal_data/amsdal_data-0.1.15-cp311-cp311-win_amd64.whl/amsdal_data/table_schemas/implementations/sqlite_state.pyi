from amsdal_data.connections.implementations.sqlite_state import SqliteStateConnection as SqliteStateConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema
from typing import Any

class SqliteStateTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service for managing SQLite table schemas.

    This service provides methods to register, update, and unregister tables in an SQLite database.
    It handles the creation of tables, indexes, and updates to table schemas.

    Attributes:
        connection (SqliteStateConnection): The connection to the SQLite database.
    """
    connection: SqliteStateConnection
    def register_table(self, table_schema: TableSchema) -> tuple[str, bool]:
        """
        Registers a table in the SQLite database.

        This method checks if a table with the specified schema already exists in the database.
        If the table exists, it updates the table schema. If the table does not exist, it creates
        the table and its indexes.

        Args:
            table_schema (TableSchema): The schema definition for the table to register.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating whether
            the table was created (True) or updated (False).
        """
    def create_index(self, table_name: str, column_name: str) -> None:
        """
        Creates an index on a specified column in a table.

        This method generates and executes an SQL statement to create an index on the specified column
        in the given table.

        Args:
            table_name (str): The name of the table where the index will be created.
            column_name (str): The name of the column to index.

        Returns:
            None
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

        This method converts the class name in the address to camel case to generate the table name.

        Args:
            address (Address): The address containing the class name to resolve.

        Returns:
            str: The resolved table name in camel case.
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_table(self, table_name: str, table_schema: TableSchema) -> None:
        """
        Creates a table in the SQLite database.

        This method generates and executes an SQL statement to create a table with the specified schema
        in the SQLite database.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema definition for the table to create.

        Returns:
            None
        """
    def update_table(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn]) -> None:
        """
        Updates the schema of a table in the SQLite database.

        This method generates and executes SQL statements to update the schema of a table
        to match the provided table schema. It adds new columns and modifies existing columns as needed.

        Args:
            table_name (str): The name of the table to update.
            table_schema (TableSchema): The new schema definition for the table.
            table_columns (list[SqlTableColumn]): The current columns of the table.

        Returns:
            None
        """
    def register_internal_tables(self) -> None: ...
    def update_internal_table(self, table_schema: TableSchema) -> None: ...
