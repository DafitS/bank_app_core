from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
import os
from bank_app.domain.services.account_service import AccountService
from bank_app.infrastructure.dependencies import get_uow_account
from api.routes.user import get_current_user
from api.schemas import AccountResponse, CreateAccountRequest, DepositRequest




router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"



@router.post("/account")
def create_account(
    data: CreateAccountRequest, str = Depends(get_current_user), account_service: AccountService = Depends(get_uow_account)
):
    account = account_service.create_account(data.user_id)

    return AccountResponse(
        account_number = account.account_number,
        user_id = account.user_id,
        amount = account.amount,
        active = account.active
    )

@router.get("/accounts")
def get_accounts(_: str = Depends(get_current_user), account_service: AccountService = Depends(get_uow_account)):
    accounts = account_service.get_accounts()

    return [
        AccountResponse(
            account_number=a.account_number,
            user_id=a.user_id,
            amount=a.amount,
            active=a.active
        )
        for a in accounts
    ]

@router.get("/account/{number}")
def get_account_by_number(number: str, _: str = Depends(get_current_user), account_service: AccountService = Depends(get_uow_account)):
    account = account_service.get_by_number(number)
    return AccountResponse(
        account_number = account.account_number,
        user_id = account.user_id,
        amount = account.amount,
        active = account.active
    )

@router.put("/account/{number}/disable")
def disable_account(number: str, _: str = Depends(get_current_user), account_service: AccountService = Depends(get_uow_account)):
    account_service.disable_account(number)
    return Response(status_code=200)

@router.put("/account/{number}/deposit")
def deposit(number: str, payload: DepositRequest, _: str = Depends(get_current_user), account_service: AccountService = Depends(get_uow_account)):
    account = account_service.deposit_account(number, payload.amount)

    return AccountResponse(
        account_number=account.account_number,
        user_id=account.user_id,
        amount=account.amount,
        active=account.active
    )