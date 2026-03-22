from uuid import uuid4
from bank_app.domain.entities.user import User
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.utils import pwd_context


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, email: str, password: str, first_name: str = "", last_name: str = "") -> User:
    
        hashed = pwd_context.hash(password)
    
        user = User(user_id=uuid4(), email=email, first_name=first_name, last_name=last_name)

        return self.user_repo.create(user, hashed)

    def get_users(self):
        return self.user_repo.list_all()
    
    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repo.get_by_id(user_id)

