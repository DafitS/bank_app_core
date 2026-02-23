from fastapi import FastAPI
from .routes import router  # routes.py w tym samym folderze

api = FastAPI(title="Bank App API")
api.include_router(router)