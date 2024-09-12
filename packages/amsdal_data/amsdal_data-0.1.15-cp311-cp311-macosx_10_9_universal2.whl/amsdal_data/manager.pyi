from amsdal_data.connections.manager import ConnectionsManager as ConnectionsManager
from amsdal_data.operations.manager import OperationsManagerBase as OperationsManagerBase
from amsdal_data.transactions.manager import AmsdalTransactionManager as AmsdalTransactionManager
from amsdal_utils.utils.singleton import Singleton

class AmsdalDataManager(metaclass=Singleton):
    """
    Manages data operations, connections, and transactions within the Amsdal system.

    This class is responsible for setting and retrieving the connection manager, operations manager,
    and transaction manager. It ensures that these managers are properly initialized and accessible
    throughout the application.
    """
    _connection_manager: ConnectionsManager
    _transaction_manager: AmsdalTransactionManager
    _operations_manager: OperationsManagerBase
    def set_connection_manager(self, connection_manager: ConnectionsManager) -> None:
        """
        Sets the connection manager and initializes the transaction manager.

        Args:
            connection_manager (ConnectionsManager): The connection manager to be set.

        Returns:
            None
        """
    def set_operations_manager(self, operations_manager: OperationsManagerBase) -> None:
        """
        Sets the operations manager.

        Args:
            operations_manager (OperationsManagerBase): The operations manager to be set.

        Returns:
            None
        """
    def get_operations_manager(self) -> OperationsManagerBase:
        """
        Retrieves the operations manager.

        Returns:
            OperationsManagerBase: The operations manager.
        """
    def get_connection_manager(self) -> ConnectionsManager:
        """
        Retrieves the connection manager.

        Returns:
            ConnectionsManager: The connection manager.
        """
    def get_transaction_manager(self) -> AmsdalTransactionManager:
        """
        Retrieves the transaction manager.

        Returns:
            AmsdalTransactionManager: The transaction manager.
        """
