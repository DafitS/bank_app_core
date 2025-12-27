import uuid
import random
from sqlalchemy import Column, Float, Integer, String, ForeignKey, BigInteger, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email = Column(String(120), unique=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    account = relationship("Accounts")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    
class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(
        BigInteger,
        primary_key=True,
        unique=True
    )
    ammount = Column(Float)

    def __repr__(self):
        return f"<Accounts(account_id={self.account_id}, ammount={self.ammount})>"
    
class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    account_id_from = Column(Integer, ForeignKey("accounts.account_id"))
    account_id_to = Column(Integer, ForeignKey("accounts.account_id"))
    date = Column(DateTime)
    amount = Column(Float) 

def __repr__(self):
        return (
            f"<Transactions("
            f"transaction_id={self.transaction_id}, "
            f"from={self.account_id_from}, "
            f"to={self.account_id_to}, "
            f"date={self.date}, "
            f"amount={self.amount}"
            f")>"
        )

