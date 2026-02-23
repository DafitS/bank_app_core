from fastapi import APIRouter, Depends, HTTPException, Response, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from bank_app.infrastructure.db import SessionLocal
from bank_app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from bank_app.infrastructure.repositories.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from bank_app.infrastructure.repositories.sqlalchemy_transaction_repository import SqlAlchemyTransactionRepository

from bank_app.domain.services.user_service import UserService
from bank_app.domain.services.account_service import AccountService
from bank_app.domain.services.transaction_service import TransactionService

from bank_app.application.auth_service import AuthService

from bank_app.domain.exceptions.custom_exceptions import AuthenticationException, NotFoundError

from bank_app.api.schemas import AccountResponse, CreateAccountRequest, CreateUserRequest, UserResponse, TransactionResponse, CreateTransactionRequest


router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_session():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(401, "Invalid token")
    return payload.get("sub")


@router.post("/register")
def register(email: str, password: str, session: Session = Depends(get_session)):
    repo = SqlAlchemyUserRepository(session)
    service = UserService(repo)
    return service.create_user(email, password)


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    repo = SqlAlchemyUserRepository(session)
    auth = AuthService(repo)
    try:
        user = auth.authenticate(email, password)
    except AuthenticationException:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = auth.create_token(user)
    return {"access_token": token}


@router.get("/users")
def users(_: str = Depends(get_current_user), session: Session = Depends(get_session)):
    repo = SqlAlchemyUserRepository(session)
    service = UserService(repo)
    users = service.get_users()
    return [
        UserResponse(user_id=u.user_id, email=u.email)
        for u in users
    ]


@router.post("/account")
def create_account(
    data: CreateAccountRequest, str = Depends(get_current_user), session: Session = Depends(get_session)
):
    account_repo = SqlAlchemyAccountRepository(session)
    user_repo = SqlAlchemyUserRepository(session)
    service = AccountService(account_repo, user_repo)
    account = service.create_account(data.user_id)

    return AccountResponse(
        account_number = account.account_number,
        user_id = account.user_id,
        amount = account.amount
    )

@router.get("/accounts")
def get_accounts(_: str = Depends(get_current_user), session: Session = Depends(get_session)):
    repo = SqlAlchemyAccountRepository(session)
    service = AccountService(repo, None)
    accounts = service.get_accounts()

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
def get_account_by_number(number: str, _: str = Depends(get_current_user), session: Session = Depends(get_session)):
    repo = SqlAlchemyAccountRepository(session)
    service = AccountService(repo, None)
    account = service.get_by_number(number)
    return AccountResponse(
        account_number = account.account_number,
        user_id = account.user_id,
        amount = account.amount,
        active = account.active
    )

@router.put("/account/{number}/disable")
def disable_account(number: str, _: str = Depends(get_current_user), session: Session = Depends(get_session)):
    repo = SqlAlchemyAccountRepository(session)
    service = AccountService(repo, None)
    service.disable_account(number)
    return Response(status_code=200)


@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    payload: CreateTransactionRequest = Body(...),
    _: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    account_repo = SqlAlchemyAccountRepository(session)
    transaction_repo = SqlAlchemyTransactionRepository(session)
    service = TransactionService(account_repo, transaction_repo)
    transaction = service.transfer(
        payload.account_from_number,
        payload.account_to_number,
        payload.amount,
    )
    
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        account_number_from=transaction.account_number_from,
        account_number_to=transaction.account_number_to,
        amount=transaction.amount,
    )


@router.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})