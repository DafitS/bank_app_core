from decimal import Decimal

from sqlalchemy import UUID

from bank_app.domain.entities import account
from bank_app.domain.services.account_service import AccountService
from bank_app.domain.services.address_service import AddressService
from bank_app.domain.services.transaction_service import TransactionService
from bank_app.infrastructure.db import SessionLocal
from bank_app.infrastructure.dependencies import get_uow_transaction
from bank_app.infrastructure.repositories.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from bank_app.infrastructure.repositories.sqlalchemy_address_repository import SqlAlchemyAddressRepository
from bank_app.infrastructure.repositories.sqlalchemy_operation_history_repository import SqlAlchemyOperationHistoryRepository
from bank_app.infrastructure.repositories.sqlalchemy_transaction_repository import SqlAlchemyTransactionRepository
from bank_app.infrastructure.uow import SQLAlchemyUnitOfWork
from bank_app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from bank_app.domain.services.user_service import UserService




with get_uow_transaction() as service:
    transaction = service.transfer(
        account_from_number="39708947848719975035314715",
        account_to_number="4974118641104482710041188",
        amount=Decimal("200.00")
    )

print(transaction)  # ✅ tylko jedna transakcja