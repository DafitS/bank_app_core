from sqlalchemy.orm import Session
from uuid import UUID
from decimal import Decimal
from bank_app.domain.entities.transaction import Transaction
from bank_app.domain.repositories.transaction_repository import TransactionRepository
from bank_app.infrastructure.orm.transaction import Transactions

class SqlAlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction, account_from_id: str, account_to_id: str) -> Transaction:
        orm = Transactions(
            transaction_id=transaction.transaction_id,
            account_id_from=account_from_id,
            account_id_to=account_to_id,
            amount=transaction.amount
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)

        return Transaction(
            transaction_id=orm.transaction_id,
            account_number_from=transaction.account_number_from,
            account_number_to=transaction.account_number_to,
            amount=orm.amount
        )