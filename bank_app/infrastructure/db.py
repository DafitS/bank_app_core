from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

database_url = os.getenv("URL")
if not database_url:
    raise RuntimeError("Database URL is not set")

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)