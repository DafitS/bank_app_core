from uuid import UUID
from pydantic import EmailStr  

class User:
    def __init__(self, user_id: UUID, email: str, first_name: str = "", last_name: str = ""):
        if not email:
            raise ValueError("Email is required")
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        if not isinstance(first_name, str):
            raise ValueError("First name must be a string")
        if not isinstance(last_name, str):
            raise ValueError("Last name must be a string")

        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}\n"