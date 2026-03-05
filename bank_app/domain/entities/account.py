from decimal import Decimal
from uuid import UUID

class Account:
    def __init__(self, account_id: str, account_number: str, user_id: UUID, amount: Decimal, active: bool):
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        self.account_id = account_id          
        self.account_number = account_number  
        self.user_id = user_id               
        self.amount = amount
        self.active = active