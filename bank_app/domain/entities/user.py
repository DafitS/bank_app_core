from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID, uuid4

class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    first_name: str
    last_name: str
    password: str


#dodac walidację hasła np min 8 znakó specjalne itp, fieldwalidator, regex

