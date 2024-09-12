from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_utils.models.data_models.address import Address

from amsdal_data.connections.base import ConnectionBase


class StateConnectionBase(ConnectionBase, ABC):
    @abstractmethod
    def insert(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts data in the scope of a transaction.

        Args:
            address (Address): The address of the object.
            data (dict[str, Any]): The object data to write.

        Returns:
            None
        """
        ...

    @abstractmethod
    def bulk_insert(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts data in the scope of a transaction.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): List of tuples with address and data to write.

        Returns:
            None
        """
        ...

    @abstractmethod
    def update(self, address: Address, data: dict[str, Any]) -> None:
        """
        Updates data in the scope of a transaction.

        Args:
            address (Address): The address of the object.
            data (dict[str, Any]): The object data to write.

        Returns:
            None
        """
        ...

    @abstractmethod
    def bulk_update(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Updates data in the scope of a transaction.

        Args:
            data (list[tuple[Address, dict[str, Any]]]): List of tuples with address and data to write.

        Returns:
            None
        """
        ...

    @abstractmethod
    def delete(self, address: Address) -> None:
        """
        Deletes data in the scope of a transaction.

        Args:
            address (Address): The address of the object.

        Returns:
            None
        """
        ...

    @abstractmethod
    def bulk_delete(self, addresses: list[Address]) -> None:
        """
        Deletes data in the scope of a transaction.

        Args:
            addresses (list[Address]): List of addresses to delete.

        Returns:
            None
        """
        ...
