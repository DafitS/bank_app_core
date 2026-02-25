from bank_app.domain.services.account_service import AccountService
from bank_app.domain.services.transaction_service import TransactionService
from bank_app.infrastructure.db import SessionLocal
from bank_app.infrastructure.repositories.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from bank_app.infrastructure.repositories.sqlalchemy_transaction_repository import SqlAlchemyTransactionRepository
from bank_app.infrastructure.uow import SQLAlchemyUnitOfWork
from bank_app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from bank_app.domain.services.user_service import UserService
from bank_app.application.auth_service import AuthService

def get_uow_user():
    with SQLAlchemyUnitOfWork(SessionLocal) as uow:
        user_repository = SqlAlchemyUserRepository(uow.session)
        
        yield UserService(user_repository)

def get_uow_auth():
    with SQLAlchemyUnitOfWork(SessionLocal) as uow:
        user_repository = SqlAlchemyUserRepository(uow.session)
        
        yield AuthService(user_repository)

def get_uow_account():
    with SQLAlchemyUnitOfWork(SessionLocal) as uow:
        account_repository = SqlAlchemyAccountRepository(uow.session)
        user_repository = SqlAlchemyUserRepository(uow.session)
        
        yield AccountService(account_repository, user_repository)

def get_uow_transaction():
    with SQLAlchemyUnitOfWork(SessionLocal) as uow:
        transaction_repository = SqlAlchemyTransactionRepository(uow.session)
        account_repository = SqlAlchemyAccountRepository(uow.session)
        
        yield TransactionService(transaction_repository, account_repository)