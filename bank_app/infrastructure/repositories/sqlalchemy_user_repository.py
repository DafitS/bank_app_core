from sqlalchemy.orm import Session
from bank_app.domain.entities.user import User
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.infrastructure.orm.user import Users

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        orm = Users(email=user.email, password=user.password)
        self.session.add(orm)
        self.session.flush()
      
        return User(user_id=orm.user_id, email=orm.email, password=orm.password)

    def get_by_id(self, user_id: str) -> User | None:
        orm = self.session.query(Users).filter_by(user_id=user_id).one_or_none()
        if not orm:
            return None
        return User(user_id=orm.user_id, email=orm.email, password=orm.password)

    def get_by_email(self, email: str) -> User | None:
        orm = self.session.query(Users).filter_by(email=email).one_or_none()
        if not orm:
            return None
        return User(user_id=orm.user_id, email=orm.email, password=orm.password)

    def list_all(self):
        users = self.session.query(Users).all()
        return [User(user_id=u.user_id, email=u.email, password=u.password) for u in users]

    def update(self, user: User) -> User:
        orm = self.session.query(Users).filter_by(user_id=user.user_id).one_or_none()
        if not orm:
            return None
        orm.email = user.email
        orm.password = user.password
        self.session.commit()
        return User(user_id=orm.user_id, email=orm.email, password=orm.password)

    def delete(self, user: User) -> None:
        orm = self.session.query(Users).filter_by(user_id=user.user_id).one_or_none()
        if orm:
            self.session.delete(orm)
            self.session.commit()