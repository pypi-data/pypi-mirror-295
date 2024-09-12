from amsdal_data.connections.base import Connectable as Connectable, ConnectionBase as ConnectionBase
from amsdal_data.connections.constants import CONNECTION_BACKEND_ALIASES as CONNECTION_BACKEND_ALIASES
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.lock.base import LockBase as LockBase
from amsdal_data.transactions.background.connections.base import WorkerConnectionBase as WorkerConnectionBase
from amsdal_utils.config.data_models.connection_config import ConnectionConfig as ConnectionConfig
from amsdal_utils.models.mixins.cached_mixin import CachedMixin
from amsdal_utils.utils.singleton import Singleton
from functools import cached_property as cached_property
from typing import Any

class ConnectionsManager(CachedMixin, metaclass=Singleton):
    """
    Manages connections for the application.

    Args:
        connection_configs (list[ConnectionConfig]): List of connection configurations.
    """
    _connection_instances: list[tuple[str, Connectable, dict[str, Any]]]
    def __init__(self, connection_configs: list[ConnectionConfig]) -> None: ...
    @cached_property
    def connections(self) -> list[Connectable]:
        """
        Returns a list of connectable objects.

        Returns:
            list[Connectable]: A list of connectable objects.
        """
    @cached_property
    def transactional_connections(self) -> list[ConnectionBase]:
        """
        Returns a list of transactional connection objects.

        Returns:
            list[ConnectionBase]: A list of transactional connection objects.
        """
    @cached_property
    def lock_connection(self) -> LockBase:
        """
        Returns the lock connection object.

        Returns:
            LockBase: The lock connection object.

        Raises:
            AmsdalConnectionError: If no lock connection is found.
        """
    def connect(self) -> None:
        """
        Establishes connections using the provided credentials.

        Returns:
            None
        """
    def prepare_connections(self) -> None:
        """
        Prepares transactional connections.

        Returns:
            None
        """
    def disconnect(self) -> None:
        """
        Disconnects all connections.

        Returns:
            None
        """
    def get_connection(self, connection_name: str) -> ConnectionBase:
        """
        Retrieves a transactional connection by its name.

        Args:
            connection_name (str): The name of the connection to retrieve.

        Returns:
            ConnectionBase: The transactional connection object.

        Raises:
            ValueError: If the connection with the specified name is not a transactional connection.
        """
    def get_worker_connection(self, connection_name: str) -> WorkerConnectionBase:
        """
        Retrieves a worker connection by its name.

        Args:
            connection_name (str): The name of the connection to retrieve.

        Returns:
            WorkerConnectionBase: The worker connection object.

        Raises:
            ValueError: If the connection with the specified name is not a worker connection.
        """
    def get_connectable(self, connection_name: str) -> Connectable:
        """
        Retrieves a connectable object by its name.

        Args:
            connection_name (str): The name of the connection to retrieve.

        Returns:
            Connectable: The connectable object.

        Raises:
            ValueError: If the connection with the specified name is not found.
        """
    @staticmethod
    def _resolve_backend_class(backend: str) -> Any: ...
