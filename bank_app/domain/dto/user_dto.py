from pydantic import BaseModel


class AddressDTO(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class UserDTORequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    address: AddressDTO


class UserDTOResponse(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    address: AddressDTO | None = None


class UserDtoUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
