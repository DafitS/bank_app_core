from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated
from decimal import Decimal

class TransactionResponse(BaseModel):
    transaction_id: UUID
    account_number_from: str
    account_number_to: str
    amount: Decimal


class CreateTransactionRequest(BaseModel):
    account_from_number: str  
    account_to_number: str    
    amount: Decimal