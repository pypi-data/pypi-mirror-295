import abc
from abc import ABC, abstractmethod
from amsdal_data.connections.base import ConnectionBase as ConnectionBase
from amsdal_utils.models.data_models.address import Address as Address
from typing import Any

class HistoricalConnectionBase(ConnectionBase, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Adds/writes data to in scope of transaction.

        Args:
            address (Address): The address of the object.
            data (dict[str, Any]): The object data to write.

        Returns:
            None
        """
    @abstractmethod
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Adds/writes data to in scope of transaction.

        Args:
            address (Address): The address of the object.
            data (list[dict[str, Any]]): The object data to write.

        Returns:
            None
        """
