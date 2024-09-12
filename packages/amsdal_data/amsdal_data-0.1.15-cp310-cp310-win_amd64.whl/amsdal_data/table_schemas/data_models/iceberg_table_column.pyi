from _typeshed import Incomplete
from collections.abc import Callable as Callable
from enum import Enum
from pydantic import BaseModel
from typing import Any, ClassVar

class IcebergDataTypes(str, Enum):
    """
    Enum representing various Iceberg data types.

    Attributes:
        BOOLEAN (str): Boolean data type.
        INT (str): Integer data type.
        BIGINT (str): Big integer data type.
        LONG (str): Long integer data type.
        FLOAT (str): Floating point data type.
        DOUBLE (str): Double precision floating point data type.
        DATE (str): Date data type.
        TIME (str): Time data type.
        TIMESTAMP (str): Timestamp data type.
        STRING (str): String data type.
        UUID (str): UUID data type.
        BINARY (str): Binary data type.
        STRUCT (str): Struct data type.
        LIST (str): List data type.
        MAP (str): Map data type.
    """
    BOOLEAN = 'boolean'
    INT = 'int'
    BIGINT = 'bigint'
    LONG = 'long'
    FLOAT = 'float'
    DOUBLE = 'double'
    DATE = 'date'
    TIME = 'time'
    TIMESTAMP = 'timestamp'
    STRING = 'string'
    UUID = 'uuid'
    BINARY = 'binary'
    STRUCT = 'struct'
    LIST = 'list'
    MAP = 'map'

python_to_iceberg_types: Incomplete

class ComplexType(BaseModel):
    """
    Represents a complex data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
    """
    to_sql: ClassVar[Callable[..., str]]
    _type_value: ClassVar[Callable[[Any, IcebergDataTypes | ComplexType], str]]
    def to_sql(self) -> str:
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """
    def _type_value(self, value: IcebergDataTypes | ComplexType) -> str: ...

class StructType(ComplexType):
    """
    Represents a struct data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
        fields (dict[str, Union[IcebergDataTypes, ComplexType]]): A dictionary of field names to their respective
            Iceberg data types or complex types.
    """
    to_sql: ClassVar[Callable[..., str]]
    fields: dict[str, IcebergDataTypes | ComplexType]
    def to_sql(self) -> str:
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """

class MapType(ComplexType):
    """
    Represents a map data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
        key_type (IcebergDataTypes): The data type of the map's keys.
        value_type (Union[IcebergDataTypes, ComplexType]): The data type of the map's values.
    """
    to_sql: ClassVar[Callable[..., str]]
    key_type: IcebergDataTypes
    value_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str:
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """

class ListType(ComplexType):
    """
    Represents a list data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
        element_type (Union[IcebergDataTypes, ComplexType]): The data type of the list's elements.
    """
    to_sql: ClassVar[Callable[..., str]]
    element_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str:
        """
        Converts the list type to its SQL representation.

        Returns:
            str: The SQL representation of the list type.
        """

class IcebergTableColumn(BaseModel):
    """
    Represents a column in an Iceberg table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the column to SQL.
        cid (int): The column identifier.
        name (str): The name of the column.
        type (Union[IcebergDataTypes, ComplexType]): The data type of the column.
        notnull (int): Indicates whether the column is not nullable (1 if not nullable, 0 otherwise).
    """
    to_sql: ClassVar[Callable[..., str]]
    _to_sql_value: ClassVar[Callable[..., str]]
    cid: int
    name: str
    type: IcebergDataTypes | ComplexType
    notnull: int
    def to_sql(self) -> str:
        """
        Converts the column to its SQL representation.

        Returns:
            str: The SQL representation of the column.
        """
    def _to_sql_value(self, value: Any) -> str: ...
    @property
    def type_sql(self) -> str:
        """
        Gets the SQL representation of the column's data type.

        Returns:
            str: The SQL representation of the column's data type.
        """
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...

class IcebergTableColumnsSchema(BaseModel):
    """
    Represents the schema of columns in an Iceberg table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the schema to SQL.
        columns (list[IcebergTableColumn]): A list of columns in the Iceberg table.
    """
    to_sql: ClassVar[Callable[..., str]]
    columns: list['IcebergTableColumn']
    def to_sql(self) -> str:
        """
        Converts the schema of columns to its SQL representation.

        Returns:
            str: The SQL representation of the schema of columns.
        """
