from collections.abc import Callable
from typing import Any
from typing import ClassVar

from pydantic import BaseModel


class SqlTableColumnsSchema(BaseModel):
    """
    Represents the schema of columns in a SQL table.

    Attributes:
        to_sql (Callable[..., str]): A class variable that holds a callable to convert the schema to SQL.
        columns (list[SqlTableColumn]): A list of columns in the SQL table.
    """

    to_sql: ClassVar[Callable[..., str]]

    columns: list['SqlTableColumn']

    def to_sql(self, column_separator: str = '`') -> str:  # type: ignore[no-redef]
        """
        Converts the schema of columns to its SQL representation.

        Args:
            column_separator (str): The character used to separate column names in the SQL statement. Defaults to '`'.

        Returns:
            str: The SQL representation of the schema of columns.
        """
        columns_statement: list[str] = []
        pks = []

        for column in self.columns:
            columns_statement.append(column.to_sql(column_separator))

            if column.pk:
                pks.append((column.name, column.pk))

        if pks:
            pks = sorted(pks, key=lambda item: item[1])
            columns_statement.append(f'PRIMARY KEY ({", ".join([pk[0] for pk in pks])})')

        return ', '.join(columns_statement)


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

    def to_sql(self, column_separator: str = '`') -> str:  # type: ignore[no-redef]
        """
        Converts the schema of columns to its SQL representation.

        Args:
            column_separator (str): The character used to separate column names in the SQL statement. Defaults to '`'.

        Returns:
            str: The SQL representation of the schema of columns.
        """
        statement = f'{column_separator}{self.name}{column_separator} {self.type.upper()}'

        if self.notnull:
            statement += ' NOT NULL'

        if self.dflt_value:
            statement += f' DEFAULT {self._to_sql_value(self.dflt_value)}'

        return statement

    def _to_sql_value(self, value: Any) -> str:  # type: ignore[no-redef]
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SqlTableColumn):
            return self.name == other.name
        return False
