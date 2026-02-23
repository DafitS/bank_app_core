from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from bank_app.domain.entities.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        """
        Create a new transaction.

        Args:
            transaction (Transaction): The transaction entity to create.

        Returns:
            Transaction: The created transaction with assigned ID.
        """
        pass

