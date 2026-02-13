import os
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

import exceptions as ex
from handler import BankAppHandler
from orm import Base
from validations_models import (
    CreateAccount,
    CreateTransaction,
    CreateUser,
    LoginUser,
    UpdateAccount,
    UpdateUser,
)

SECRET_KEY: str | None = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM: str = "HS256"

security = HTTPBearer()
api = FastAPI()
bank = BankAppHandler()


@api.on_event("startup")
def create_tables_on_startup():
    Base.metadata.create_all(bind=bank.engine)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> str:
    """Validate JWT token and return user email.

    Args:
        credentials: HTTP authorization credentials.

    Returns:
        Email extracted from JWT token.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError as err:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        ) from err

    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    return user_email


@api.get("/users")
def list_users(
    _user_email: str = Depends(get_current_user),
) -> list[dict]:
    """Return list of all users."""
    return bank.get_users()


@api.delete("/user/{user_id}")
def delete_user(
    user_id: UUID,
    _user_email: str = Depends(get_current_user),
) -> Response:
    """Delete user by ID."""
    try:
        bank.delete_user(str(user_id))
        return Response(status_code=200)
    except ex.NotFoundError as err:
        raise HTTPException(
            status_code=404,
            detail="Not found error!",
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail="Internal error!",
        ) from err


@api.post("/register")
def create_user(body: CreateUser) -> dict:
    """Register new user."""
    try:
        return bank.create_user(**body.model_dump())
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=str(err),
        ) from err


@api.put("/user")
def update_user(
    body: UpdateUser,
    _user_email: str = Depends(get_current_user),
) -> dict:
    """Update user email."""
    return bank.update_user(**body.model_dump())


@api.post("/account")
def create_account(
    body: CreateAccount,
    _user_email: str = Depends(get_current_user),
) -> dict:
    """Create bank account."""
    return bank.create_account(**body.model_dump())


@api.post("/transaction")
def create_transaction(
    body: CreateTransaction,
    _user_email: str = Depends(get_current_user),
) -> Response:
    """Create money transaction between accounts."""
    try:
        bank.create_transaction(**body.model_dump())
        return Response(status_code=200)
    except ex.NotFoundError as err:
        raise HTTPException(
            status_code=404,
            detail="Not found error!",
        ) from err
    except (
        ex.ErrorConversionType,
        ex.AmountTooSmallError,
    ) as err:
        raise HTTPException(
            status_code=400,
            detail="Conversion amount error!",
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail="Internal error!",
        ) from err


@api.get("/accounts")
def list_accounts(
    _user_email: str = Depends(get_current_user),
) -> list[dict]:
    """Return list of accounts."""
    return bank.get_accounts()


@api.delete("/account/{number}")
def delete_account(
    number: str,
    _user_email: str = Depends(get_current_user),
) -> Response:
    """Delete account by account number."""
    try:
        bank.delete_account(number)
        return Response(status_code=200)
    except ex.NotFoundError as err:
        raise HTTPException(
            status_code=404,
            detail="Not found error!",
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from err


@api.put("/account")
def update_account(
    body: UpdateAccount,
    _user_email: str = Depends(get_current_user),
) -> dict:
    """Update account balance."""
    try:
        return bank.update_account(**body.model_dump())
    except ex.NotFoundError as err:
        raise HTTPException(
            status_code=404,
            detail="Not found error!",
        ) from err
    except (
        ex.ErrorConversionType,
        ex.AmountTooSmallError,
    ) as err:
        raise HTTPException(
            status_code=400,
            detail="Conversion amount error!",
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from err


@api.post("/login")
def login_user(body: LoginUser) -> str:
    """Authenticate user and return JWT token."""
    try:
        user = bank.authenticate(**body.model_dump())
    except ex.AuthenticationException as err:
        raise HTTPException(
            status_code=401,
            detail="UNAUTHORIZED!",
        ) from err

    return bank.create_access_token(
        data={"sub": user.email},
        expires_minutes=15,
    )


@api.get("/health")
def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"})
