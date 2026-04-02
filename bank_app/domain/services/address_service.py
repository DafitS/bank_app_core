from uuid import UUID, uuid4

from bank_app.domain.entities.address import Address
from bank_app.domain.dto.address_dto import AddressDTORequest, AddressDTOResponse
class AddressService:
    def __init__(self, address_repo):
        self.address_repo = address_repo

    def create_address(self, AddressDtoRequest) -> AddressDTOResponse:

        current_addresses = self.address_repo.get_by_user_id(AddressDtoRequest.user_id)
        for addr in current_addresses:
            addr.is_current = False
            self.address_repo.update(addr)


        address = Address(
            user_id=AddressDtoRequest.user_id,
            street=AddressDtoRequest.street,
            city=AddressDtoRequest.city,
            state=AddressDtoRequest.state,
            zip_code=AddressDtoRequest.zip_code,
            is_current=True
        )
        saved_address = self.address_repo.create(address)

        return AddressDTOResponse(
            address_id=str(saved_address.address_id),
            user_id=str(saved_address.user_id),
            street=saved_address.street,
            city=saved_address.city,
            state=saved_address.state,
            zip_code=saved_address.zip_code,
            is_current=saved_address.is_current
        )

    def get_addresses_by_user_id(self, user_id: UUID):
        return self.address_repo.get_by_user_id(user_id)
    
    def get_address_by_id(self, address_id: UUID):
        return self.address_repo.get_by_id(address_id)
    
    def update_address(self, address_id: UUID, street: str, city: str, state: str, zip_code: str):
        address = self.address_repo.get_by_id(address_id)
        if not address:
            raise ValueError("Address not found")

        address.street = street
        address.city = city
        address.state = state
        address.zip_code = zip_code

        return self.address_repo.update(address)

        