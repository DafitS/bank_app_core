from uuid import UUID
from pydantic import EmailStr  

class User:
    def __init__(self, user_id: UUID, email: str, password: str):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password cannot be empty")

        self.user_id = user_id
        self.email = email
        self.password = password  