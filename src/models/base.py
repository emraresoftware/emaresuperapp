"""
Emare SuperApp — Base Model Mixin
Tüm modellerin ortak alanları.
"""
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from datetime import datetime


class BaseModel(Base):
    """Soyut temel model — id, created_at, updated_at otomatik eklenir."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
