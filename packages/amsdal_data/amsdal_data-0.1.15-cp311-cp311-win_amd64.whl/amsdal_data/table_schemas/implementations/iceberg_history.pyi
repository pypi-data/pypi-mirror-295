from _typeshed import Incomplete
from amsdal_data.connections.implementations.iceberg_history import IcebergHistoricalConnection as IcebergHistoricalConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.iceberg_table_column import ComplexType as ComplexType, IcebergTableColumn as IcebergTableColumn, IcebergTableColumnsSchema as IcebergTableColumnsSchema
from amsdal_data.transactions.constants import TRANSACTION_CLASS_NAME as TRANSACTION_CLASS_NAME
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableColumnSchema, TableSchema

address_struct: Incomplete
reference_struct: Incomplete

class IcebergTableColumnSchema(TableColumnSchema):
    """
    Represents a schema for an Iceberg table column.

    Attributes:
        type (type | ComplexType): The data type of the column, which can be a basic type or a complex type.
    """
    type: type | ComplexType

class IcebergHistoryTableSchemaService(TableSchemaServiceBase):
    """
    Service class for managing Iceberg table schemas.

    Attributes:
        connection (IcebergHistoricalConnection): The connection to the Iceberg historical database.
    """
    connection: IcebergHistoricalConnection
    def register_table(self, table_schema: TableSchema) -> tuple[str, bool]:
        """
        Registers a table in the Iceberg historical database.

        Args:
            table_schema (TableSchema): The schema of the table to register.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating if the table was created.
        """
    def resolve_table_name(self, address: Address) -> str:
        """
        Resolves the table name based on the given address.

        Args:
            address (Address): The address object containing class name and version information.

        Returns:
            str: The resolved table name.
        """
    def _build_create_table_statement(self, table_name: str, table_schema: TableSchema) -> str: ...
    def create_table(self, table_name: str, table_schema: TableSchema) -> None:
        """
        Creates a table in the Iceberg historical database.

        Args:
            table_name (str): The name of the table to create.
            table_schema (TableSchema): The schema of the table to create.

        Returns:
            None
        """
    def unregister_table(self, address: Address) -> None: ...
    def register_internal_tables(self) -> None:
        """
        Registers internal tables in the Iceberg historical database.

        This method registers a set of predefined internal tables required for the Iceberg historical database.
        If the tables already exist, it updates them to match the current schema definitions.

        Returns:
            None
        """
    def update_internal_table(self, table_schema: TableSchema) -> None:
        """
        Updates an internal table in the Iceberg historical database.

        This method updates the schema of an existing internal table to match the provided table schema.
        It adds new columns and drops columns that are no longer present in the schema.

        Args:
            table_schema (TableSchema): The schema of the table to update.

        Returns:
            None
        """
