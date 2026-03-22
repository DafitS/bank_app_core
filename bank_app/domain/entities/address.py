from uuid import UUID


class Address:
    def __init__(self, address_id: UUID, user_id: UUID, street: str, city: str, state: str, zip_code: str):
        self.address_id = address_id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return (
            f"Address("
            f"id={self.address_id}, "
            f"user_id={self.user_id}, "
            f"street={self.street}, "
            f"city={self.city}, "
            f"state={self.state}, "
            f"zip={self.zip_code})"
            "\n"
        )