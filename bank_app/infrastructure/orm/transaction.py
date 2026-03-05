from sqlalchemy import Column, Numeric, String, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id_from = Column(String(36), ForeignKey("accounts.account_id", ondelete="CASCADE"), nullable=False)
    account_id_to   = Column(String(36), ForeignKey("accounts.account_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(20,2), nullable=False)

    account_from = relationship("Accounts", foreign_keys=[account_id_from])
    account_to = relationship("Accounts", foreign_keys=[account_id_to])

    __table_args__ = (CheckConstraint("amount > 0"),)