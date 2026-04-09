import uuid
from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from bank_app.infrastructure.orm import user_roles


class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    role_name = Column(String(120), unique=True, nullable=False)

    role_users = relationship(
        "UserRoles",
        back_populates="role"
    )

    

    
