import string
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from datetime import datetime
from uuid import UUID

class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must have 8 or more symbols!")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have a lowercase letter!")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have an uppercase letter!")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have a digit!")
        if not any(c in string.punctuation for c in value):
            raise ValueError("Password must have a special character!")
        return value


class CreateAccount(BaseModel):
    user_id: UUID


class UpdateUser(BaseModel):
    user_id: UUID
    new_email: EmailStr


class CreateTransaction(BaseModel):
    account_from: str
    account_to: str
    amount: float = Field(..., gt=0)
    date: datetime

    @model_validator(mode="after")
    def validate_accounts(cls, model):
        if model.account_from == model.account_to:
            raise ValueError("Accounts must be different!")
        return model
    


class UpdateAccount(BaseModel):
    number: str
    new_amount: float

    @field_validator("new_amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0!")
        return value

class LoginUser(BaseModel):
    email: str
    password: str