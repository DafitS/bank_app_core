import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    accounts = relationship(
        "Accounts",
        back_populates="user",
    )