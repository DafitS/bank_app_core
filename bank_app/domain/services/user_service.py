from uuid import UUID, uuid4
from bank_app.domain.dto.user_dto import UserDTORequest, UserDTOResponse
from bank_app.domain.entities.address import Address
from bank_app.domain.entities.user import User
from bank_app.domain.repositories.address_repository import AddressRepository
from bank_app.domain.repositories.user_repository import UserRepository
from bank_app.utils import pwd_context


class UserService:
    def __init__(self, user_repo: UserRepository, address_repo: AddressRepository):
        self.user_repo = user_repo
        self.address_repo = address_repo

    def create_user(self, user_dto: UserDTORequest) -> UserDTOResponse:
    
        hashed = pwd_context.hash(user_dto.password)
    
        user = User(
            email=user_dto.email,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            password=hashed
        )

        return_user =  self.user_repo.create(user)

        address = Address(
            address_id=uuid4(),
            user_id=return_user.user_id,
            street=user_dto.address.street,
            city=user_dto.address.city,
            state=user_dto.address.state,
            zip_code=user_dto.address.zip_code
        )
        self.address_repo.create(address)

        user_dto_response = UserDTOResponse(
            user_id=str(return_user.user_id),
            email=return_user.email,
            first_name=return_user.first_name,
            last_name=return_user.last_name,
            address=user_dto.address
        )

        return user_dto_response


    def get_users(self):
        return self.user_repo.list_all()
    
    def get_user_by_id(self, user_id: UUID) -> User | None:
        return self.user_repo.get_by_id(user_id)

