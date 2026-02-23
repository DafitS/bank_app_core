from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.domain.services.user_service import UserService
from bank_app.domain.exceptions.custom_exceptions import AuthenticationException
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.user_service = UserService(user_repo)

    def authenticate(self, email: str, password: str):
     
        try:
            user = self.user_service.authenticate_user(email, password)
            return user
        except AuthenticationException as e:
            raise AuthenticationException(str(e))

    def create_token(self, user):
        payload = {"sub": str(user.user_id), "email": user.email}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token