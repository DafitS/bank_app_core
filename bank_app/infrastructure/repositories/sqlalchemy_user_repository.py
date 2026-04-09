from sqlalchemy import UUID
from sqlalchemy.orm import Session

from bank_app.domain.entities.user import User
from bank_app.domain.exceptions.custom_exceptions import NotFoundError
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.infrastructure.orm.user import Users


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        orm = Users(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        self.session.add(orm)
        self.session.flush()

        return User(
            user_id=orm.user_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            password=orm.password,
        )

    def get_by_id(self, user_id: UUID) -> User | None:
        orm = (
            self.session.query(Users)
            .filter_by(user_id=user_id)
            .one_or_none()
        )
        if not orm:
            return None
        return User(
            user_id=orm.user_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            password=orm.password,
        )

    def get_by_email(self, email: str) -> User | None:
        orm = (
            self.session.query(Users)
            .filter_by(email=email)
            .one_or_none()
        )
        if not orm:
            return None
        return User(
            user_id=orm.user_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            password=orm.password,
        )

    def list_all(self):
        users = self.session.query(Users).all()
        return [
            User(
                user_id=u.user_id,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                password=u.password,
            )
            for u in users
        ]

    def update(self, user: User) -> User:
        orm = (
            self.session.query(Users)
            .filter_by(user_id=user.user_id)
            .one_or_none()
        )
        if not orm:
            raise NotFoundError("User not found")

        orm.email = user.email
        orm.password = user.password
        orm.first_name = user.first_name
        orm.last_name = user.last_name

        self.session.flush()

        return User(
            user_id=orm.user_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            password=orm.password,
        )

    def delete(self, user: User) -> None:
        orm = (
            self.session.query(Users)
            .filter_by(user_id=user.user_id)
            .one_or_none()
        )
        if orm:
            self.session.delete(orm)
            self.session.flush()
