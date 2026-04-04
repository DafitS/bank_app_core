import uuid

from bank_app.application.mappers.account_mapper import AccountMapper
from bank_app.domain.dto.account_dto import AccountDTORequest, AccountDTOResponse
from bank_app.infrastructure.orm.operation_history import OperationHistory
from bank_app.domain.repositories.operation_history_repository import OperationHistoryRepository
from bank_app.utils import generate_unique_account_number
from bank_app.domain.entities.account import Account
from bank_app.domain.exceptions.custom_exceptions import NotFoundError, AmountTooSmallError
from uuid import UUID
from decimal import Decimal
class AccountService:

    def __init__(self, account_repo, user_repo, operation_repo):
        self.account_repo = account_repo
        self.user_repo = user_repo
        self.operation_repo = operation_repo

    def create_account(self, dto: AccountDTORequest) -> AccountDTOResponse:
        user = self.user_repo.get_by_id(dto.user_id)
        if not user:
            raise NotFoundError("User not found")

        account = AccountMapper.to_entity(dto)

        saved_account = self.account_repo.create(account)
        return AccountMapper.to_dto(saved_account)

    def get_accounts(self) -> list[AccountDTOResponse]:
        accounts = self.account_repo.list_all()
        return [AccountMapper.to_dto(account) for account in accounts]

    def get_by_number(self, number: str) -> AccountDTOResponse:
        account = self.account_repo.get_by_number(number)
        if not account:
            raise NotFoundError("Account not found")
        
        return AccountMapper.to_dto(account)

    def disable_account(self, number: str) -> None:
        account = self.account_repo.get_by_number(number)

        if not account:
            raise NotFoundError("Account not found")

        self.account_repo.disable(account)
    
    def withdraw_account(self, number: str, amount: Decimal):
        account = self.account_repo.get_by_number(number)
        if not account:
            raise NotFoundError("Account not found")
        if not account.active:
            raise NotFoundError("Account is inactive")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if account.amount < Decimal(str(amount)):
            raise AmountTooSmallError("Insufficient funds")

        account.amount -= Decimal(str(amount))
        updated_account = self.account_repo.update(account)

        operation = OperationHistory(
            operation_id=uuid.uuid4(),
            account_id=account.account_id,
            operation_type="withdraw",
            amount=amount
        )

        self.operation_repo.create(operation)

        return AccountMapper.to_dto(updated_account)
    
    def deposit_account(self, number: str, amount: Decimal):
        account = self.account_repo.get_by_number(number)
        if not account:
            raise NotFoundError("Account not found")
        if not account.active:
            raise NotFoundError("Account is inactive")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        account.amount += Decimal(str(amount))
        updated_account = self.account_repo.update(account)

        operation = OperationHistory(
            operation_id=uuid.uuid4(),
            account_id=account.account_id,
            operation_type="deposit",
            amount=amount
        )

        self.operation_repo.create(operation)

        return AccountMapper.to_dto(updated_account)
        