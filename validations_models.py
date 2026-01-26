from pydantic import BaseModel, Field, model_validator, EmailStr
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr

class UpdateUser(BaseModel):
    user_id: str
    new_email: EmailStr

class CreateTransaction(BaseModel):
    account_from: str
    account_to: str
    amount: float = Field(...,gt=0)
    date: datetime
    
    @model_validator(mode="after")
    def validdate_accounts(self):
        if self.account_from == self.account_to:
            raise ValueError("Accounts must be different!")
        else:
            return self



class UpdateAccount(BaseModel):
     number: str
     new_amount: float

class CreateAccount(BaseModel):
    user_id: str
