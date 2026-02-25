from fastapi import FastAPI
from .routes import router
from bank_app.domain.exceptions.global_handler_exceptions import register_exception_handlers

api = FastAPI(title="Bank App API")
api.include_router(router)

register_exception_handlers(api)