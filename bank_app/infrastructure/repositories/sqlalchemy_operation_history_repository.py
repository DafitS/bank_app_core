
from uuid import UUID

from sqlalchemy.orm import Session
from bank_app.domain.repositories.operation_history_repository import OperationHistoryRepository
from bank_app.domain.entities.operation_history import OperationHistory
from bank_app.infrastructure.orm.operation_history import OperationHistory as OperationHistoryORM


class SqlAlchemyOperationHistoryRepository(OperationHistoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, operation_history: OperationHistory) -> OperationHistory:
        self.session.add(operation_history)
        self.session.flush()
        self.session.refresh(operation_history)
        return operation_history

    def get_by_id(self, operation_id: UUID) -> OperationHistory:
        
            operation_history_searched = self.session.query(OperationHistoryORM).filter(OperationHistoryORM.operation_id == operation_id).first()

            if operation_history_searched is None:
                return None
            
            return OperationHistory(
                id=operation_history_searched.operation_id,
                account_id=operation_history_searched.account_id,
                operation_type=operation_history_searched.operation_type,
                amount=operation_history_searched.amount,
                account_from_id=operation_history_searched.account_from_id,
                account_to_id=operation_history_searched.account_to_id,
                created_at=operation_history_searched.created_at
            )


    def get_by_account_id(self, account_id: UUID):
       
            operations_searched = self.session.query(OperationHistoryORM).filter(OperationHistoryORM.account_id == account_id).all()

            return [
                OperationHistory(
                    id=operation.operation_id,
                    account_id=operation.account_id,
                    operation_type=operation.operation_type,
                    amount=operation.amount,
                    account_from_id=operation.account_from_id,
                    account_to_id=operation.account_to_id,
                    created_at=operation.created_at
                ) for operation in operations_searched
            ]
            
           
        