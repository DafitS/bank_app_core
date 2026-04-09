import re

from pydantic import BaseModel, field_validator


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

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Min 8 znaków")

        if not re.search(r"[a-z]", value):
            raise ValueError("Brak małej litery")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Brak wielkiej litery")

        if not re.search(r"\d", value):
            raise ValueError("Brak cyfry")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Brak znaku specjalnego")

        return value
    #password: str = Field(pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$') -- brak wsparcia w pydantic v2


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
