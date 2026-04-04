from bank_app.domain.entities.address import Address
from bank_app.domain.dto.address_dto import AddressDTORequest, AddressDTOResponse

class AddressMapper:

    @staticmethod
    def to_dto(address: Address) -> AddressDTOResponse:
        return AddressDTOResponse(
            address_id=str(address.address_id),
            user_id=str(address.user_id),
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            is_current=address.is_current
        )

    @staticmethod
    def from_request(dto: AddressDTORequest) -> Address:
        return Address(
            user_id=dto.user_id,
            street=dto.street,
            city=dto.city,
            state=dto.state,
            zip_code=dto.zip_code,
            is_current=True
        )