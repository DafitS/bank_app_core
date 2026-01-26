from sqlalchemy import create_engine
from orm import Base


engine = create_engine("postgresql://admin:1234@localhost:5433/bank_app_core")


Base.metadata.create_all(bind=engine)

print("✅ Tabele zostały utworzone!")