from amsdal_data.connections.implementations.postgresql_history import PostgresHistoricalConnection as PostgresHistoricalConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_data.transactions.constants import TRANSACTION_CLASS_NAME as TRANSACTION_CLASS_NAME
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema
from typing import Any

class PostgresHistoricalTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service for managing PostgreSQL historical table schemas.

    This service provides methods to register, unregister, and update table schemas in a PostgreSQL historical database.
    It also includes functionality to handle internal tables and their schemas.

    Attributes:
        connection (PostgresHistoricalConnection): The connection to the PostgreSQL historical database.
        TABLE_SEPARATOR (str): The separator used in table names.
        COLUMN_SEPARATOR (str): The separator used in column names.
    """
    connection: PostgresHistoricalConnection
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    @staticmethod
    def _to_sql_type(type_: Any) -> str: ...
    def register_table(self, table_schema: TableSchema, *, is_internal_table: bool = False) -> tuple[str, bool]:
        """
        Registers a table in the PostgreSQL historical database.

        This method checks if a table with the given schema already exists in the database.
        If the table exists, it returns the table name and a flag indicating that the table was not created.
        If the table does not exist, it creates the table and returns the table name and a flag indicating that
            the table was created.

        Args:
            table_schema (TableSchema): The schema of the table to register.
            is_internal_table (bool, optional): Flag indicating if the table is an internal table. Defaults to False.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a flag indicating if the table was created.
        """
    def create_index(self, table_name: str, column_name: str) -> None:
        """
        Creates an index on a specified column in a table.

        This method builds and executes a SQL statement to create an index on the specified column
        of the given table in the PostgreSQL historical database.

        Args:
            table_name (str): The name of the table on which to create the index.
            column_name (str): The name of the column on which to create the index.

        Returns:
            None
        """
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table from the PostgreSQL historical database.

        This method removes a table with the given address from the database by executing a SQL statement to drop
            the table.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name for a given address.

        This method converts the class name and version from the address into a table name.
        If the class name matches the transaction class name, it returns the class name in lowercase.
        If the class version is the latest, it retrieves the latest class version and includes it in the table name.

        Args:
            address (Address): The address containing the class name and version.

        Returns:
            str: The resolved table name.
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_table(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False) -> None:
        """
        Creates a table in the PostgreSQL historical database.

        This method builds and executes a SQL statement to create a table with the specified schema.
        It also handles the creation of internal tables if specified.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema of the table to create.
            is_internal_table (bool, optional): Flag indicating if the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def register_internal_tables(self) -> None:
        """
        Registers internal tables in the PostgreSQL historical database.

        This method registers a set of predefined internal tables required for the PostgreSQL historical database.
        If the tables already exist, it updates them to match the current schema definitions.

        Returns:
            None
        """
    def update_internal_table(self, table_schema: TableSchema) -> None:
        """
        Updates an internal table in the PostgreSQL historical database.

        This method updates the schema of an existing internal table to match the provided table schema.
        It adds new columns and drops columns that are no longer present in the schema.

        Args:
            table_schema (TableSchema): The schema of the table to update.

        Returns:
            None
        """
