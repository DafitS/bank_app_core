from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class TransactionDTORequest(BaseModel):
    account_number_from: str
    account_number_to: str
    amount: Decimal

class TransactionDTOResponse(BaseModel):
    transaction_id: str
    account_number_from: str
    account_number_to: str
    amount: Decimal
    created_at: datetime | None = None