from uuid import UUID

from pydantic import BaseModel


class AddressDTORequest(BaseModel):
    user_id: UUID
    street: str
    city: str
    state: str
    zip_code: str

class AddressDTOResponse(BaseModel):
    address_id: str
    user_id: str
    street: str
    city: str
    state: str
    zip_code: str
    is_current: bool