import exceptions as ex
from fastapi import FastAPI, HTTPException, Response
from handler import BankAppHandler
from uuid import UUID
from fastapi.responses import JSONResponse
from validations_models import CreateUser, CreateTransaction, CreateAccount, UpdateAccount, UpdateUser, LoginUser
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import timezone

security = HTTPBearer()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
    user_email = token_decoded.get("sub")
    if user_email is None:
        raise HTTPException(status_code=401, message = "Invalid Token!")
    return user_email



api = FastAPI()
bank = BankAppHandler()



@api.get("/users")
def list_users(user_email: str = Depends(get_current_user)):
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
         
@api.post("/register")
def create_user(body: CreateUser):
    return bank.create_user(**body.model_dump())

@api.put("/user")
def update_user(body: UpdateUser):
    return bank.update_user(**body.model_dump())

@api.post("/account")
def create_account(body: CreateAccount, user_email: str = Depends(get_current_user)):
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
    

@api.post("/login")
def login_user(body: LoginUser):
    try:
        user =  bank.authenticate(**body.model_dump())
    except ex.AuthenticationException:
        raise HTTPException(status_code=401, detail="UNATHORIZED!") 

    return bank.create_access_token(data={"sub": user.email}, expires_minutes=15)
    
        


@api.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})