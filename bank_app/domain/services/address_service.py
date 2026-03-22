from uuid import uuid4

from bank_app.domain.entities.address import Address

class AddressService:
    def __init__(self, address_repo):
        self.address_repo = address_repo

    def create_address(self, user_id: str, street: str, city: str, state: str, zip_code: str):
        address = Address(
            address_id=uuid4(),
            user_id=user_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        return self.address_repo.create(address)

    def get_addresses_by_user_id(self, user_id: str):
        return self.address_repo.get_by_user_id(user_id)