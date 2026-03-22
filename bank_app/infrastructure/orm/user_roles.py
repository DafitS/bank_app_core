from sqlalchemy import Column, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from bank_app.infrastructure.orm.base import Base

class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id = Column(ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(ForeignKey("roles.role_id"), primary_key=True)

    user = relationship(
        "Users",
        back_populates="user_roles"
    )

    role = relationship(
        "Roles",
        back_populates="role_users"
    )