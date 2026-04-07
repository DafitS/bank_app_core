from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Address(BaseModel):
    address_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    street: str
    city: str
    state: str
    zip_code: str
    is_current: bool = True
