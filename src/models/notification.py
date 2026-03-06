"""
Emare SuperApp — Notification Modeli
"""
from sqlalchemy import String, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from .base import BaseModel
import enum


class NotificationChannel(str, enum.Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"


class Notification(BaseModel):
    """Bildirim kaydı."""

    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    channel: Mapped[str] = mapped_column(Enum(NotificationChannel), default=NotificationChannel.IN_APP)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    action_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<Notification '{self.title}' → user={self.user_id}>"
