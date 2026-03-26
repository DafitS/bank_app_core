from datetime import datetime
from decimal import Decimal
from uuid import UUID

class Transaction:
    def __init__(self, transaction_id: UUID, account_number_from: str, account_number_to: str, amount: Decimal, created_at=None):
        
        self._validate_uuid_id_exists(transaction_id, "transaction_id")
        self._validate_account_number(account_number_from, "account_number_from")           
        self._validate_account_number(account_number_to, "account_number_to")
        self._validate_amount(amount)
        self._validate_accounts_different(account_number_from, account_number_to)
        self._validate_created_at(created_at)


        self.transaction_id = transaction_id
        self.account_number_from = account_number_from
        self.account_number_to = account_number_to
        self.amount = amount
        self.created_at = created_at
        

    def _validate_uuid_id_exists(self, value, field_name):
        if value is not None and not isinstance(value, UUID):
            raise ValueError(f"{field_name} must be a valid UUID")

    def _validate_account_number(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")

    def _validate_amount(self, amount):
        if not isinstance(amount, Decimal):
            raise ValueError("amount must be Decimal")
        if amount <= 0:
            raise ValueError("Transaction amount must be > 0")

    def _validate_accounts_different(self, from_acc, to_acc):
        if from_acc == to_acc:
            raise ValueError("Sender and receiver accounts cannot be the same")

    def _validate_created_at(self, created_at):
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("created_at must be datetime")
        
        
    def __repr__(self):
        return (
            f"Transaction(id={self.transaction_id}, "
            f"from={self.account_number_from}, "
            f"to={self.account_number_to}, "
            f"amount={self.amount})"
            f"created_at={self.created_at})"
        )