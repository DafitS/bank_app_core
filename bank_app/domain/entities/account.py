from decimal import Decimal
from uuid import UUID


class Account:
    def __init__(
        self,
        account_id: str,
        account_number: str,
        user_id: UUID,
        amount: Decimal,
        active: bool = True,
    ):
        self._validate_account_id_if_exists(account_id)
        self._validate_account_number(account_number)
        self._validate_user_id(user_id)
        self._validate_amount(amount)
        self._validate_active(active)

        self.account_id = account_id
        self.account_number = account_number
        self.user_id = user_id
        self.amount = amount
        self.active = active

    @staticmethod
    def _validate_account_id_if_exists(account_id):
        if account_id is not None and (
            not isinstance(account_id, str) or not account_id
        ):
            raise ValueError("account_id must be a non-empty string")

    @staticmethod
    def _validate_account_number(account_number):
        if not isinstance(account_number, str) or not account_number:
            raise ValueError("account_number must be a non-empty string")

    @staticmethod
    def _validate_user_id(user_id):
        if not isinstance(user_id, UUID):
            raise ValueError("user_id must be a valid UUID")

    @staticmethod
    def _validate_amount(amount):
        if not isinstance(amount, Decimal):
            raise ValueError("amount must be Decimal")
        if amount < 0:
            raise ValueError("Amount cannot be negative")

    @staticmethod
    def _validate_active(active):
        if not isinstance(active, bool):
            raise ValueError("active must be a boolean")

    def __repr__(self):
        return (
            f"Account(id={self.account_id}, "
            f"number={self.account_number}, "
            f"user_id={self.user_id}, "
            f"amount={self.amount}, "
            f"active={self.active})"
        )
