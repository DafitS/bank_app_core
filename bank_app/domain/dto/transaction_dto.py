from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


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
