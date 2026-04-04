from uuid import UUID, uuid4

from bank_app.application.mappers.address_mapper import AddressMapper
from bank_app.domain.entities.address import Address
from bank_app.domain.dto.address_dto import AddressDTORequest, AddressDTOResponse
class AddressService:
    def __init__(self, address_repo):
        self.address_repo = address_repo


    def create_address(self, address_dto: AddressDTORequest) -> AddressDTOResponse:

        current_addresses = self.address_repo.get_by_user_id(address_dto.user_id)
        for addr in current_addresses:
            addr.is_current = False
            self.address_repo.update(addr)


        address = AddressMapper.from_request(address_dto)
        saved_address = self.address_repo.create(address)

        return AddressMapper.to_dto(saved_address)


    def get_addresses_by_user_id(self, user_id: UUID):
        addresses = self.address_repo.get_by_user_id(user_id)
        return [AddressMapper.to_dto(addr) for addr in addresses]
    
    
    def get_address_by_id(self, address_id: UUID):
        address = self.address_repo.get_by_id(address_id)
        if not address:
            return None
        
        return AddressMapper.to_dto(address)

    
    def update_address(self, address_id: UUID, street: str, city: str, state: str, zip_code: str):
        address = self.address_repo.get_by_id(address_id)
        if not address:
            return None

        address.street = street
        address.city = city
        address.state = state
        address.zip_code = zip_code

        updated_address = self.address_repo.update(address)
        return AddressMapper.to_dto(updated_address)

        