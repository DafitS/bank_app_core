from fastapi import APIRouter, Depends, HTTPException, Response, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials   
from typing import Annotated
from jose import JWTError, jwt
import os
from bank_app.application.auth_service import AuthService
from bank_app.domain.services.user_service import UserService
from bank_app.infrastructure.dependencies import get_uow_user, get_uow_auth
from bank_app.domain.exceptions.custom_exceptions import AuthenticationException
from api.schemas import UserResponse


router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"



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
def register(email: str, password: str, user_service: UserService = Depends(get_uow_user)):
    return user_service.create_user(email, password)


@router.post("/login")
def login(email: str, password: str, auth_service: AuthService = Depends(get_uow_auth)):
    try:
        user = auth_service.authenticate(email, password)
    except AuthenticationException:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = auth_service.create_token(user)
    return {"access_token": token}


@router.get("/users")
def users(_: str = Depends(get_current_user), user_service: UserService = Depends(get_uow_user)):
    users = user_service.get_users()
    return [
        UserResponse(user_id=u.user_id, email=u.email)
        for u in users
    ]
