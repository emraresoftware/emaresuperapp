"""Notifications Schemas — bildirim Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Bildirim Gönderme
# ---------------------------------------------------------------------------

class NotificationSendRequest(BaseModel):
    """Tekil bildirim gönderme isteği."""

    user_id: str
    title: str = Field(..., max_length=200)
    body: str = Field(..., max_length=2000)
    notification_type: str = Field("info", pattern="^(info|warning|success|error)$")
    data: dict[str, Any] | None = None


class BulkNotificationRequest(BaseModel):
    """Toplu bildirim gönderme isteği."""

    user_ids: list[str] = Field(..., min_length=1)
    title: str = Field(..., max_length=200)
    body: str = Field(..., max_length=2000)
    notification_type: str = Field("info", pattern="^(info|warning|success|error)$")
    data: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Bildirim Yanıtı
# ---------------------------------------------------------------------------

class NotificationSchema(BaseModel):
    """Bildirim detay yanıtı."""

    id: str
    user_id: str
    title: str
    body: str
    type: str
    data: dict[str, Any] | None = None
    is_read: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Liste Yanıtı
# ---------------------------------------------------------------------------

class NotificationListResponse(BaseModel):
    """Sayfalı bildirim listesi yanıtı."""

    items: list[NotificationSchema] = Field(default_factory=list)
    page: int = 1
    page_size: int = 20
    total: int = 0
    unread_count: int = 0


# ---------------------------------------------------------------------------
# Toplu Gönderim Yanıtı
# ---------------------------------------------------------------------------

class BulkSendResponse(BaseModel):
    """Toplu bildirim gönderim sonucu."""

    sent_count: int
    notification_ids: list[str]
