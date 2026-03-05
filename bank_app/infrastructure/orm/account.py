from sqlalchemy import Column, String, Numeric, ForeignKey, Boolean, DateTime
from .base import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship

class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_number = Column(String(32), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    amount = Column(Numeric(20, 2), nullable=False)
    active = Column(Boolean, default=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("Users", back_populates="accounts")