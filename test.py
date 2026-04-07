from decimal import Decimal

from sqlalchemy import UUID

from bank_app.domain.entities import account
from bank_app.domain.services.account_service import AccountService
from bank_app.domain.services.address_service import AddressService
from bank_app.domain.services.transaction_service import TransactionService
from bank_app.infrastructure.db import SessionLocal
from bank_app.infrastructure.dependencies import get_uow_transaction, get_uow_user
from bank_app.infrastructure.repositories.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from bank_app.infrastructure.repositories.sqlalchemy_address_repository import SqlAlchemyAddressRepository
from bank_app.infrastructure.repositories.sqlalchemy_operation_history_repository import SqlAlchemyOperationHistoryRepository
from bank_app.infrastructure.repositories.sqlalchemy_transaction_repository import SqlAlchemyTransactionRepository
from bank_app.infrastructure.uow import SQLAlchemyUnitOfWork
from bank_app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from bank_app.domain.services.user_service import UserService
from bank_app.domain.dto.user_dto import UserDTORequest, UserDTOResponse


from bank_app.domain.dto.user_dto import UserDTORequest, AddressDTO

user = UserDTORequest(
    email="testtt@example.pl",
    password="Secure12s3!",
    first_name="Jan",
    last_name="Kowalski",
    address=AddressDTO(
        street="ul. Główna 123",
        city="Warszawa",
        state="Mazowieckie",
        zip_code="00-001"
    )
)
with get_uow_user() as user_service:
        user = user_service.create_user(user)
        print(user)

        
       

       
    

