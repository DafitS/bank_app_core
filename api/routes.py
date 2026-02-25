from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse

import os

from bank_app.infrastructure.db import SessionLocal



router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"




@router.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})