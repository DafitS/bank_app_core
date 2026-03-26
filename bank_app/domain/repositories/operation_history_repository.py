from abc import ABC, abstractmethod

from sqlalchemy import UUID
from bank_app.domain.entities.operation_history import OperationHistory

class OperationHistoryRepository(ABC):
    
    @abstractmethod
    def create(self, operation_history: OperationHistory) -> OperationHistory:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, operation_id: UUID) -> OperationHistory:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_account_id(self, account_id: UUID):
        raise NotImplementedError