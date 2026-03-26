from uuid import UUID


class Address:
    def __init__(self, address_id: UUID, user_id: UUID, street: str, city: str, state: str, zip_code: str):

        self._validate_uuid_if_exists(address_id, "address_id")
        self._validate_uuid_if_exists(user_id, "user_id")
        self._validate_string(street, "street")
        self._validate_string(city, "city")
        self._validate_string(state, "state")
        self._validate_string(zip_code, "zip_code")


        self.address_id = address_id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def _validate_uuid_if_exists(self, value, field_name):
        if value is not None and not isinstance(value, UUID):
            raise ValueError(f"{field_name} must be a valid UUID")

    def _validate_string(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")



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