from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


class AccountDTORequest(BaseModel):
    user_id: UUID


class AccountDTOResponse(BaseModel):
    account_id: str
    account_number: str
    user_id: UUID
    amount: Decimal
    active: bool