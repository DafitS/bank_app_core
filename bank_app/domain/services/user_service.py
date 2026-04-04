from uuid import UUID, uuid4
from bank_app.application.mappers.user_mapper import UserMapper
from bank_app.domain.dto.user_dto import UserDTORequest, UserDTOResponse, UserDtoUpdate
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

       

        return UserMapper.to_dto(return_user, address)


    def get_users(self) -> list[UserDTOResponse]:
        users = self.user_repo.list_all()

        user_dtos = []
        for user in users:
            address = self.address_repo.get_by_user_id(user.user_id)
            user_dtos.append(UserMapper.to_dto(user, address))

        return user_dtos
    
    def get_user_by_id(self, user_id: UUID) -> UserDTOResponse | None:
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            return None
        
        address = self.address_repo.get_by_user_id(user_id)

        return UserMapper.to_dto(user, address)

    def get_user_by_email(self, email: str) -> UserDTOResponse | None:
        user = self.user_repo.get_by_email(email)
        
        if not user:
            return None
        
        address = self.address_repo.get_by_user_id(user.user_id)

        return UserMapper.to_dto(user, address)

    def update_user(self, user_id: UUID, user_dto: UserDtoUpdate) -> UserDTOResponse | None:
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            return None
        
        if user_dto.first_name is not None:
            user.first_name = user_dto.first_name
        if user_dto.last_name is not None:
            user.last_name = user_dto.last_name
        if user_dto.email is not None:
            user.email = user_dto.email
        if user_dto.password is not None:
            user.password = pwd_context.hash(user_dto.password)

        updated_user = self.user_repo.update(user)
        address = self.address_repo.get_by_user_id(user_id)

        return UserMapper.to_dto(updated_user, address)