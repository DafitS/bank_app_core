from sqlalchemy import UUID

from bank_app.domain.services.account_service import AccountService
from bank_app.domain.services.address_service import AddressService
from bank_app.infrastructure.db import SessionLocal
from bank_app.infrastructure.repositories.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from bank_app.infrastructure.repositories.sqlalchemy_address_repository import SqlAlchemyAddressRepository
from bank_app.infrastructure.uow import SQLAlchemyUnitOfWork
from bank_app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from bank_app.domain.services.user_service import UserService

uow = SQLAlchemyUnitOfWork(SessionLocal)
with uow:
    user_repo = SqlAlchemyUserRepository(uow.session)
    user_service = UserService(user_repo)

    repo_address = SqlAlchemyAddressRepository(uow.session)
    account_repo = SqlAlchemyAccountRepository(uow.session)   
    
    account_service = AccountService(account_repo, user_repo)

    account = account_service.get_by_number("3970847848719975035314715")

    print(account)
   