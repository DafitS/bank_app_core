from uuid import uuid4
from bank_app.domain.entities.user import User
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.utils import pwd_context
from bank_app.domain.exceptions.custom_exceptions import AuthenticationException

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, email: str, password: str) -> User:
        # Hashujemy hasło
        hashed = pwd_context.hash(password)

        # Tworzymy obiekt User z wygenerowanym UUID
        user = User(user_id=uuid4(), email=email, password=hashed)

        # Zapis do repozytorium
        return self.user_repo.create(user)

    def get_users(self):
        return self.user_repo.list_all()

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise AuthenticationException("User not found")

        if not pwd_context.verify(password, user.password):
            raise AuthenticationException("Wrong password")

        return user