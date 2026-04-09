from datetime import datetime

import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from bank_app.infrastructure.orm.base import Base

class OperationHistory(Base):
    __tablename__ = "operation_history"

    operation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(ForeignKey("accounts.account_id"), nullable=True)
    account_from_id = Column(ForeignKey("accounts.account_id"), nullable=True)
    account_to_id = Column(ForeignKey("accounts.account_id"), nullable=True)
    operation_type = Column(String, nullable=False) 
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    account_from = relationship(
        "Accounts",
        foreign_keys=[account_from_id]
    )

    account_to = relationship(
        "Accounts",
        foreign_keys=[account_to_id]
    )