from decimal import Decimal
from uuid import UUID

class Account:
    def __init__(self, account_id: str, account_number: str, user_id: UUID, amount: Decimal, active: bool = True):
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        self.account_id = account_id          
        self.account_number = account_number  
        self.user_id = user_id               
        self.amount = amount
        self.active = active

    def __repr__(self):
        return (
            f"Account(id={self.account_id}, "
            f"number={self.account_number}, "
            f"user_id={self.user_id}, "
            f"amount={self.amount}, "
            f"active={self.active})"
        )