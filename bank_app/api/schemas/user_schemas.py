from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)