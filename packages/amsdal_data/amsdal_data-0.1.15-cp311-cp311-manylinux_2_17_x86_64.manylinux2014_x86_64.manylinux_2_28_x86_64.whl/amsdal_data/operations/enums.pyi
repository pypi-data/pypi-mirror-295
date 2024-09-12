from enum import Enum

class OperationType(Enum):
    """
    Enum representing different types of operations.

    Attributes:
        CREATE: Represents a create operation.
        UPDATE: Represents an update operation.
        DELETE: Represents a delete operation.
    """
    CREATE = ...
    UPDATE = ...
    DELETE = ...
