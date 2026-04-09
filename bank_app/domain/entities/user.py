import re
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator


class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    first_name: str
    last_name: str
    password: str





