from _typeshed import Incomplete
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.connections.manager import ConnectionsManager as ConnectionsManager
from amsdal_data.data_models.transaction_context import TransactionContext as TransactionContext
from amsdal_data.transactions.errors import AmsdalTransactionError as AmsdalTransactionError
from amsdal_utils.utils.singleton import Singleton
from typing import Any

logger: Incomplete

class AmsdalTransactionManager(metaclass=Singleton):
    context: Incomplete
    transaction_object: Incomplete
    connection_manager: Incomplete
    def __init__(self, connection_manager: ConnectionsManager) -> None: ...
    def begin(self, context: TransactionContext, transaction_kwargs: dict[str, Any]) -> None:
        """
        Begins a transaction.

        Args:
            context (TransactionContext): The context of the transaction.
            transaction_kwargs (dict[str, Any]): The keyword arguments for the transaction.

        Returns:
            None
        """
    def commit(self, return_value: Any) -> None:
        """
        Commits (stores) the transaction to the database.

        Args:
            return_value (Any): The return value of the transaction.

        Returns:
            None

        Raises:
            AmsdalTransactionError: If there is no ongoing transaction or if the transaction commit fails.
        """
    def rollback(self) -> None:
        """
        Rolls back the transaction.

        Args:
            None

        Returns:
            None
        """
