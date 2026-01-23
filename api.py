import exceptions as ex
from fastapi import FastAPI, HTTPException, Response
from handler import BankAppHandler
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from fastapi.responses import JSONResponse

api = FastAPI()
bank = BankAppHandler()

class CreateUser(BaseModel):
    email: str

class UpdateUser(BaseModel):
    user_id: str
    new_email: str

class CreateTransaction(BaseModel):
    account_from: str
    account_to: str
    amount: float
    date: datetime

class UpdateAccount(BaseModel):
     number: str
     new_amount: float

class CreateAccount(BaseModel):
    user_id: str

@api.get("/users")
def list_users():
    return bank.get_users()

@api.delete("/user/{user_id}")
def delete_user(user_id: UUID):
    try:        
        bank.delete_user(str(user_id))
        return Response(status_code=200)
    except ex.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Not found error!")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error!")
         
@api.post("/user")
def create_user(body: CreateUser):
    return bank.create_user(**body.model_dump())

@api.put("/user")
def update_user(body: UpdateUser):
    return bank.update_user(**body.model_dump())

@api.post("/account")
def create_account(body: CreateAccount):
    return bank.create_account(**body.model_dump())

@api.post("/transaction")
def create_transaction(body: CreateTransaction):
    try:
        bank.create_transaction(**body.model_dump())
        return Response(status_code=200)
    except ex.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Not found error!")
    except (ex.ErrorConversionType, ex.AmountTooSmallError) as e:
        raise HTTPException(status_code=400, detail="Conversion amount error!")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error!")
    
@api.get("/accounts")
def list_accounts():
    return bank.get_accounts()

@api.delete("/account/{number}")
def delete_account(number: str):
    try:
        bank.delete_account(number)
        return Response(status_code=200)
    except ex.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Not found error!")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

class UpdateAccount(BaseModel):
    number: str
    new_amount: float

@api.put("/account")
def update_account(body: UpdateAccount):
    try:
        return bank.update_account(**body.model_dump())
    except ex.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Not found error!")
    except (ex.ErrorConversionType, ex.AmountTooSmallError) as e:
        raise HTTPException(status_code=400, detail="Conversion amount error!")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})