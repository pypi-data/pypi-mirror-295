from collections.abc import Callable
from datetime import date
from datetime import datetime
from enum import Enum
from typing import Any
from typing import ClassVar
from typing import Union

from pydantic import BaseModel


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


python_to_iceberg_types = {
    bool: IcebergDataTypes.BOOLEAN,
    int: IcebergDataTypes.LONG,
    float: IcebergDataTypes.DOUBLE,
    str: IcebergDataTypes.STRING,
    bytes: IcebergDataTypes.BINARY,
    date: IcebergDataTypes.DATE,
    datetime: IcebergDataTypes.TIMESTAMP,
}


class ComplexType(BaseModel):
    """
    Represents a complex data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
    """

    to_sql: ClassVar[Callable[..., str]]
    _type_value: ClassVar[Callable[[Any, Union[IcebergDataTypes, 'ComplexType']], str]]

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """
        return 'string'

    def _type_value(self, value: Union[IcebergDataTypes, 'ComplexType']) -> str:  # type: ignore[no-redef]
        return value.to_sql() if isinstance(value, ComplexType) else value.value


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

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """
        return 'struct<{}>'.format(', '.join(f'{k}: {self._type_value(v)}' for k, v in self.fields.items()))


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

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the complex type to its SQL representation.

        Returns:
            str: The SQL representation of the complex type.
        """
        return f'map<{self.key_type.value}, {self._type_value(self.value_type)}>'


class ListType(ComplexType):
    """
    Represents a list data type in Iceberg.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the type to SQL.
        element_type (Union[IcebergDataTypes, ComplexType]): The data type of the list's elements.
    """

    to_sql: ClassVar[Callable[..., str]]

    element_type: IcebergDataTypes | ComplexType

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the list type to its SQL representation.

        Returns:
            str: The SQL representation of the list type.
        """
        return f'array<{self._type_value(self.element_type)}>'


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

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the column to its SQL representation.

        Returns:
            str: The SQL representation of the column.
        """
        statement = f'{self.name} {self.type_sql}'
        if self.notnull:
            statement += ' NOT NULL'

        return statement

    def _to_sql_value(self, value: Any) -> str:  # type: ignore[no-redef]
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)

    @property
    def type_sql(self) -> str:
        """
        Gets the SQL representation of the column's data type.

        Returns:
            str: The SQL representation of the column's data type.
        """
        if isinstance(self.type, ComplexType):
            return self.type.to_sql()

        if self.type == IcebergDataTypes.MAP:
            return 'map<string, string>'
        return self.type.value

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, IcebergTableColumn):
            return self.name == other.name
        return False


class IcebergTableColumnsSchema(BaseModel):
    """
    Represents the schema of columns in an Iceberg table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the schema to SQL.
        columns (list[IcebergTableColumn]): A list of columns in the Iceberg table.
    """

    to_sql: ClassVar[Callable[..., str]]

    columns: list['IcebergTableColumn']

    def to_sql(self) -> str:  # type: ignore[no-redef]
        """
        Converts the schema of columns to its SQL representation.

        Returns:
            str: The SQL representation of the schema of columns.
        """
        columns_statement: list[str] = []

        for column in self.columns:
            columns_statement.append(column.to_sql())

        return ', '.join(columns_statement)
