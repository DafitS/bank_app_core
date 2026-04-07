from decimal import Decimal
from uuid import uuid4

from bank_app.domain.dto.account_dto import AccountDTORequest, AccountDTOResponse
from bank_app.domain.entities.account import Account
from bank_app.utils import generate_unique_account_number


class AccountMapper:
    @staticmethod
    def to_dto(account: Account) -> AccountDTOResponse:
        return AccountDTOResponse(
            account_id=account.account_id,
            account_number=account.account_number,
            user_id=account.user_id,
            amount=account.amount,
            active=account.active
        )

    @staticmethod
    def to_entity(dto: AccountDTORequest) -> Account:
        return Account(
            account_id=str(uuid4()),
            account_number=str(generate_unique_account_number()),
            user_id=dto.user_id,
            amount=Decimal(0),
        )
