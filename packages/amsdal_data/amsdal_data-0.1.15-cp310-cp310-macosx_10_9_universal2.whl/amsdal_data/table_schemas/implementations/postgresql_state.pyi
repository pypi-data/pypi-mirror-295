from amsdal_data.connections.implementations.postgresql_state import PostgresStateConnection as PostgresStateConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema
from typing import Any

class PostgresStateTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service for managing PostgreSQL table schemas.

    This service provides methods to register, update, and unregister tables in a PostgreSQL database.
    It also handles the creation of indexes and the resolution of table names.

    Attributes:
        connection (PostgresStateConnection): The connection to the PostgreSQL database.
        TABLE_SEPARATOR (str): The separator used for table names.
        COLUMN_SEPARATOR (str): The separator used for column names.
    """
    connection: PostgresStateConnection
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    @staticmethod
    def _to_sql_type(type_: Any) -> str: ...
    def register_table(self, table_schema: TableSchema, *, is_internal_table: bool = False) -> tuple[str, bool]:
        """
        Registers a set of predefined internal tables required for the PostgreSQL historical database.

        This method registers a set of predefined internal tables required for the PostgreSQL historical database.
        If the tables already exist, it updates them to match the current schema definitions.

        Returns:
            None
        """
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
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table from the PostgreSQL database.

        This method drops the table corresponding to the provided address from the PostgreSQL database.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name from an address.

        This method converts the class name of the provided address to camel case to form the table name.

        Args:
            address (Address): The address from which to resolve the table name.

        Returns:
            str: The resolved table name.
        """
    def update_table(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn]) -> None:
        """
        Updates the schema of an existing table.

        This method generates and executes SQL statements to update the schema of an existing table
        to match the provided table schema. It adds new columns and modifies existing columns as needed.

        Args:
            table_name (str): The name of the table to update.
            table_schema (TableSchema): The new schema definition for the table.
            table_columns (list[SqlTableColumn]): The current columns of the table.

        Returns:
            None
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_table(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False) -> None:
        """
        Creates a table in the PostgreSQL database.

        This method generates and executes a SQL statement to create a table with the specified schema.
        It can optionally mark the table as an internal table.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema definition for the table.
            is_internal_table (bool, optional): Whether the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def register_internal_tables(self) -> None: ...
    def update_internal_table(self, table_schema: TableSchema) -> None: ...
