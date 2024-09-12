from amsdal_data.connections.implementations.postgresql_immutable import PostgresImmutableConnection as PostgresImmutableConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn
from amsdal_data.table_schemas.implementations.mixins.sql_statements_mixin import SqlStatementsMixin as SqlStatementsMixin
from amsdal_data.transactions.constants import TRANSACTION_CLASS_NAME as TRANSACTION_CLASS_NAME
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema
from typing import Any

class PostgresImmutableTableSchemaService(SqlStatementsMixin, TableSchemaServiceBase):
    """
    Service class for managing PostgreSQL immutable table schemas.

    This class provides methods to register, update, and unregister tables in a PostgreSQL database.
    It also includes functionality to handle internal tables and build SQL statements for table operations.

    Attributes:
        connection (PostgresImmutableConnection): The connection to the PostgreSQL database.
        TABLE_SEPARATOR (str): The separator used for table names in SQL statements.
        COLUMN_SEPARATOR (str): The separator used for column names in SQL statements.
    """
    connection: PostgresImmutableConnection
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    @staticmethod
    def _to_sql_type(type_: Any) -> str: ...
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name for a given address.

        This method converts the class name from the address into a table name by converting it to lowercase.

        Args:
            address (Address): The address containing the class name.

        Returns:
            str: The resolved table name in lowercase.
        """
    def register_table(self, table_schema: TableSchema, *, is_internal_table: bool = False) -> tuple[str, bool]:
        """
        Registers a table in the PostgreSQL database.

        This method checks if a table with the given schema already exists. If it does, the table is updated to match
            the schema.
        If it does not exist, a new table is created. Indexes are also created for the table based on the schema.

        Args:
            table_schema (TableSchema): The schema of the table to register.
            is_internal_table (bool, optional): Flag indicating if the table is an internal table. Defaults to False.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating if the table was created.
        """
    def _build_create_index_statement(self, table_name: str, index_name: str, columns: list[str]) -> str: ...
    def create_index(self, table_name: str, column_name: str) -> None:
        """
        Creates an index on a specified column in a table.

        This method builds and executes a SQL statement to create an index on the given column of the specified table.
        If the index already exists, it will not be created again.

        Args:
            table_name (str): The name of the table on which to create the index.
            column_name (str): The name of the column on which to create the index.

        Returns:
            None
        """
    def update_table(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn], *, is_internal_table: bool = False) -> None:
        """
        Updates a table in the PostgreSQL database.

        This method updates the schema of an existing table to match the provided table schema.
        It adds new columns and drops columns that are no longer present in the schema.

        Args:
            table_name (str): The name of the table to update.
            table_schema (TableSchema): The schema of the table to update.
            table_columns (list[SqlTableColumn]): The current columns of the table.
            is_internal_table (bool, optional): Flag indicating if the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def _build_update_table_statements(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn], *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[str]: ...
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table from the PostgreSQL database.

        This method drops the table corresponding to the given address from the database.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    @staticmethod
    def _build_select_table_name_statement(table_name: str) -> tuple[str, list[Any]]: ...
    def create_table(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False) -> None:
        """
        Creates a table in the PostgreSQL database.

        This method builds and executes a SQL statement to create a table with the given schema.
        If the table already exists, it will not be created again.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema of the table to create.
            is_internal_table (bool, optional): Flag indicating if the table is an internal table. Defaults to False.

        Returns:
            None
        """
    def _build_columns_from_schema(self, table_schema: TableSchema, *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[SqlTableColumn]: ...
    def register_internal_tables(self) -> None:
        """
        Registers a set of predefined internal tables required for the PostgreSQL historical database.

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
