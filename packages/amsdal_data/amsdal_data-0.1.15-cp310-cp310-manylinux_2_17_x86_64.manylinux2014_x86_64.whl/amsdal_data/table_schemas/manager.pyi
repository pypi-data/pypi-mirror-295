from _typeshed import Incomplete
from amsdal_data.manager import AmsdalDataManager as AmsdalDataManager
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.transactions.manager import AmsdalTransactionManager as AmsdalTransactionManager
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.singleton import Singleton

class TableSchemasManager(metaclass=Singleton):
    _tables: Incomplete
    _schemas_cache: Incomplete
    _schemas_map: Incomplete
    _schemas_reverse_map: Incomplete
    def __init__(self) -> None: ...
    def set_schemas_cache(self, class_name: str, schema: TableSchema) -> None:
        """
        Sets the schema cache for a given class name and schema.

        This method updates the schema cache, schema map, and reverse schema map for the specified class name
        and schema. It ensures that the latest version and the specific version of the schema are stored.

        Args:
            class_name (str): The name of the class for which the schema cache is being set.
            schema (TableSchema): The schema definition to cache.

        Returns:
            None
        """
    def get_schemas_map(self, class_name: str, class_version: str | Versions) -> dict[str, str] | None:
        """
        Retrieves the schema map for a given class name and version.

        This method returns the schema map, which is a dictionary mapping column names to field IDs,
        for the specified class name and version. If the schema map does not exist, it returns None.

        Args:
            class_name (str): The name of the class for which the schema map is being retrieved.
            class_version (str | Versions): The version of the class for which the schema map is being retrieved.

        Returns:
            dict[str, str] | None: The schema map for the specified class name and version, or None if it does not exist
        """
    def get_schemas_reverse_map(self, class_name: str, class_version: str | Versions) -> dict[str, str] | None:
        """
        Retrieves the reverse schema map for a given class name and version.

        This method returns the reverse schema map, which is a dictionary mapping field IDs to column names,
        for the specified class name and version. If the reverse schema map does not exist, it returns None.

        Args:
            class_name (str): The name of the class for which the reverse schema map is being retrieved.
            class_version (str | Versions): The version of the class for which the reverse schema map is being retrieved

        Returns:
            dict[str, str] | None: The reverse schema map for the specified class name and version, or None if it does
                not exist.
        """
    def register_table(self, table_schema: TableSchema) -> tuple[str, bool]:
        """
        Checks, registers, and creates a new table in the database through the connection.

        This method verifies if the table schema is already registered. If not, it registers the table
        using the appropriate table schema service and updates the schema cache.

        Args:
            table_schema (TableSchema): The schema definition for the table to register.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating whether
            the table was created (True) or updated (False).
        """
    def unregister_table(self, address: Address) -> None:
        """
        Unregisters a table in the database.

        This method removes the table registration for the specified address using the appropriate
        table schema services.

        Args:
            address (Address): The address of the table to unregister.

        Returns:
            None
        """
    @staticmethod
    def resolve_table_schema_services(address: Address) -> list[TableSchemaServiceBase]:
        """
        Resolves the table schema services for a given address.

        This method determines the appropriate table schema services based on the provided address.
        It retrieves the transaction manager and the lakehouse configuration to identify the relevant
        table schema services.

        Args:
            address (Address): The address for which to resolve the table schema services.

        Returns:
            list[TableSchemaServiceBase]: A list of table schema services corresponding to the provided address.
        """
