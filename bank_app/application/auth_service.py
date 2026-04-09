import os

from jose import jwt

from bank_app.domain.entities.user import User
from bank_app.domain.exceptions.custom_exceptions import AuthenticationException
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.utils import pwd_context

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, email: str, password: str):

        try:
            user = self.authenticate_user(email, password)
            return user
        except AuthenticationException as e:
            raise AuthenticationException(str(e)) from e

    def create_token(self, user):
        payload = {"sub": str(user.user_id), "email": user.email}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise AuthenticationException("User not found")

        if not pwd_context.verify(password, user.password):
            raise AuthenticationException("Wrong password")

        return user
