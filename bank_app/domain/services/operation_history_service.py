

from uuid import UUID


class OperationHistoryService:
    def __init__(self, operation_history_repository):
        self.operation_history_repository = operation_history_repository

    def get_operation_history(self, account_id: UUID):
        return self.operation_history_repository.get_by_account_id(account_id)
    
    def get_operation_by_id(self, operation_id: UUID):
        return self.operation_history_repository.get_by_id(operation_id)