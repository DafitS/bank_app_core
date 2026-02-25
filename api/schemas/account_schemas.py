from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class AccountResponse(BaseModel):
    account_number: str
    user_id: UUID
    amount: float
    active: bool


class CreateAccountRequest(BaseModel):
    user_id: UUID
    amount: float = Field(ge=0, default=0.0)

class DepositRequest(BaseModel):
    amount: float