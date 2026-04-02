import uuid

from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship

from bank_app.infrastructure.orm.base import Base

class Addresses(Base):
    __tablename__ = "addresses"

    address_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    street = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    zip_code = Column(String(20), nullable=False)
    is_current = Column(Boolean, default=True)

    user = relationship("Users", back_populates="addresses")