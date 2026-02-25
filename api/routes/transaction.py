from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBearer 
import os
from bank_app.domain.services.transaction_service import TransactionService
from bank_app.infrastructure.dependencies import get_uow_transaction
from api.routes.user import get_current_user
from api.schemas import CreateTransactionRequest, TransactionResponse



router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    payload: CreateTransactionRequest = Body(...),
    _: str = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_uow_transaction)
):
    transaction_service.transfer(
        payload.account_from_number,
        payload.account_to_number,
        payload.amount  
    )    
    
    return TransactionResponse(
            account_number_from=payload.account_from_number,
            account_number_to=payload.account_to_number,
            amount=payload.amount
        )
