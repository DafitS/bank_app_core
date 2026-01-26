import uuid
from utils import generate_nanoid
from sqlalchemy import Column, Float, Integer, Numeric, String, ForeignKey, BigInteger, DateTime, func, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    accounts = relationship("Accounts", back_populates="user")


    
class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(
        String(12),
        primary_key=True,
        default=generate_nanoid
    )

    account_number = Column(
        Numeric(26, 0),
        unique=True,
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False
    )

    amount = Column(Float, default=0.0)

    user = relationship("Users", back_populates="accounts")

    transactions_from = relationship("Transactions", foreign_keys="Transactions.account_id_from", backref="from_account")
    transactions_to = relationship("Transactions", foreign_keys="Transactions.account_id_to", backref="to_account")
    
class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    account_id_from = Column(
    String(12),
    ForeignKey("accounts.account_id", ondelete="CASCADE"),
    nullable=False
)

    account_id_to = Column(
        String(12),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False
)


    date = Column(DateTime,
         default=func.now(), 
         nullable=False)
    
    amount = Column(Float,
         nullable=False) 

    __table_args__ = (
        CheckConstraint("amount > 0", name = "invalid_range_value_amount"),
    )



