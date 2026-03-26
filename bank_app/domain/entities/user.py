from uuid import UUID
from email_validator import validate_email, EmailNotValidError
class User:
    def __init__(self, user_id: UUID, email: str, first_name: str = "", last_name: str = ""):
        
        self._validate_uuid_if_exists(user_id, "user_id")
        self._validate_email(email)
        self._validate_string(first_name, "first_name")
        self._validate_string(last_name, "last_name")



        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


    def _validate_uuid_if_exists(self, value, field_name):
        if value is not None and not isinstance(value, UUID):
            raise ValueError(f"{field_name} must be a valid UUID")

    def _validate_email(self, email):
        try:
            valid = validate_email(email)  # walidacja emaila
            self.email = valid.email       # normalizuje email np. usuwa spacje
        except EmailNotValidError:
            raise ValueError(f"Invalid email format: {email}")

    def _validate_string(self, value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        

    def __repr__(self):
        return f"Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}\n"