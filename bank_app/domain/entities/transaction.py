from decimal import Decimal
from uuid import UUID

class Transaction:
    def __init__(self, transaction_id: UUID, account_number_from: str, account_number_to: str, amount: Decimal):
        if amount <= 0:
            raise ValueError("Transaction amount must be > 0")
        if account_number_from == account_number_to:
            raise ValueError("Sender and receiver accounts cannot be the same")
        self.transaction_id = transaction_id
        self.account_number_from = account_number_from
        self.account_number_to = account_number_to
        self.amount = amount