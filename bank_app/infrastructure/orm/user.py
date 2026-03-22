from datetime import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from bank_app.infrastructure.orm import user_roles


class Users(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)



    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = relationship(
        "Accounts",
        back_populates="user",
    )

    user_roles = relationship(
        "UserRoles",
        back_populates="user"
    )

    addresses = relationship(
        "Addresses", 
        back_populates="user",
        uselist=False
    )