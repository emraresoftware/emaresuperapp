"""
Emare SuperApp — User & Role Modelleri
"""
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from .base import BaseModel

# Many-to-many: User <-> Role
user_roles = Table(
    "user_roles",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    extend_existing=True,  # Test ortamında çift import'a karşı koruma
)


class Role(BaseModel):
    """Kullanıcı rolü."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    users: Mapped[List["User"]] = relationship(
        secondary=user_roles, back_populates="roles"
    )

    def __repr__(self):
        return f"<Role {self.name}>"


class User(BaseModel):
    """Kullanıcı modeli."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    roles: Mapped[List[Role]] = relationship(
        secondary=user_roles, back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.username}>"
