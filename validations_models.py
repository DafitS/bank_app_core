import string
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

MIN_PASSWORD_LENGTH: int = 8


class CreateUser(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate password complexity.

        Rules:
        - minimum length
        - at least one lowercase letter
        - at least one uppercase letter
        - at least one digit
        - at least one special character

        Args:
            value: Raw password string.

        Returns:
            Validated password.

        Raises:
            ValueError: If password does not meet requirements.
        """
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                f"Password must have at least "
                f"{MIN_PASSWORD_LENGTH} characters!"
            )
        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain a lowercase letter!"
            )
        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain an uppercase letter!"
            )
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain a digit!")
        if not any(c in string.punctuation for c in value):
            raise ValueError(
                "Password must contain a special character!"
            )

        return value


class CreateAccount(BaseModel):
    """Schema for creating a bank account."""

    user_id: UUID


class UpdateUser(BaseModel):
    """Schema for updating user email."""

    user_id: UUID
    new_email: EmailStr


class CreateTransaction(BaseModel):
    """Schema for creating a transaction between accounts."""

    account_from_id: str
    account_to_id: str
    amount: float = Field(..., gt=0)

    @model_validator(mode="after")
    def validate_accounts(self) -> "CreateTransaction":
        """Ensure source and destination accounts are different.

        Returns:
            Validated transaction model.

        Raises:
            ValueError: If accounts are the same.
        """
        if self.account_from_id == self.account_to_id:
            raise ValueError("Accounts must be different!")

        return self


class UpdateAccount(BaseModel):
    """Schema for updating account balance."""

    number: str
    new_amount: float

    @field_validator("new_amount")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        """Validate account balance value.

        Args:
            value: New account amount.

        Returns:
            Validated amount.

        Raises:
            ValueError: If amount is not greater than zero.
        """
        if value <= 0:
            raise ValueError("Amount must be greater than 0!")

        return value


class LoginUser(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str
