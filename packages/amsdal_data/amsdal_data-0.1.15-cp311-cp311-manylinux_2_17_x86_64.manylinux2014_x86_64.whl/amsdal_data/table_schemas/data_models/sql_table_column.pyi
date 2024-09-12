from collections.abc import Callable as Callable
from pydantic import BaseModel
from typing import Any, ClassVar

class SqlTableColumnsSchema(BaseModel):
    """
    Represents the schema of columns in a SQL table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the schema to SQL.
        columns (list[SqlTableColumn]): A list of columns in the SQL table.
    """
    to_sql: ClassVar[Callable[..., str]]
    columns: list['SqlTableColumn']
    def to_sql(self, column_separator: str = '`') -> str:
        """
        Converts the schema of columns to its SQL representation.

        Args:
            column_separator (str): The character used to separate column names in the SQL statement. Defaults to '`'.

        Returns:
            str: The SQL representation of the schema of columns.
        """

class SqlTableColumn(BaseModel):
    """
    Represents a column in a SQL table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the column to SQL.
        cid (int): The column identifier.
        name (str): The name of the column.
        type (str): The data type of the column.
        notnull (int): Indicates whether the column is not nullable (1 if not nullable, 0 otherwise).
        dflt_value (Any): The default value of the column.
        pk (int): Indicates whether the column is a primary key (1 if primary key, 0 otherwise).
    """
    to_sql: ClassVar[Callable[..., str]]
    _to_sql_value: ClassVar[Callable[..., str]]
    cid: int
    name: str
    type: str
    notnull: int
    dflt_value: Any
    pk: int
    def to_sql(self, column_separator: str = '`') -> str:
        """
        Converts the schema of columns to its SQL representation.

        Args:
            column_separator (str): The character used to separate column names in the SQL statement. Defaults to '`'.

        Returns:
            str: The SQL representation of the schema of columns.
        """
    def _to_sql_value(self, value: Any) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
