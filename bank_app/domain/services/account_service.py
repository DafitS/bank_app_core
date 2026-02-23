from bank_app.utils import generate_unique_account_number
from bank_app.domain.entities.account import Account
from bank_app.domain.exceptions.custom_exceptions import NotFoundError, AmountTooSmallError
from uuid import UUID
from decimal import Decimal
class AccountService:

    def __init__(self, account_repo, user_repo):
        self.account_repo = account_repo
        self.user_repo = user_repo

    def create_account(self, user_id: UUID) -> Account:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        from uuid import uuid4

        account = Account(
            account_id=str(uuid4()),             
            account_number=str(generate_unique_account_number()),
            user_id=user_id,
            amount=Decimal(0),
        )

        return self.account_repo.create(account)

    def get_accounts(self):
        return self.account_repo.list_all()

    def get_by_number(self, number):
        account = self.account_repo.get_by_number(number)
        if not account:
            raise NotFoundError("Account not found")
        return account
    def disable_account(self, number: str) -> None:
        account = self.account_repo.get_by_number(number)

        if not account:
            raise NotFoundError("Account not found")

        self.account_repo.disable(account)