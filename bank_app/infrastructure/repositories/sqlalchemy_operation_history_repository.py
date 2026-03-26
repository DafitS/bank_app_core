
from uuid import UUID

from sqlalchemy.orm import Session
from bank_app.domain.repositories.operation_history_repository import OperationHistoryRepository
from bank_app.infrastructure.orm.operation_history import OperationHistory


class SqlAlchemyOperationHistoryRepository(OperationHistoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, operation_history: OperationHistory) -> OperationHistory:
        self.session.add(operation_history)
        self.session.flush()
        self.session.refresh(operation_history)
        return operation_history

    def get_by_id(self, operation_id: UUID) -> OperationHistory:
        return (
            self.session.query(OperationHistory)
            .filter(OperationHistory.id == operation_id)
            .first()
        )

    def get_by_account_id(self, account_id: UUID):
        return (
            self.session.query(OperationHistory)
            .filter(OperationHistory.account_id == account_id)
            .all()
        )