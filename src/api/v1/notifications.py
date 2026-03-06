"""
Emare SuperApp — Notifications API Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class NotificationResponse(BaseModel):
    id: int
    title: str
    body: Optional[str] = None
    channel: str = "in_app"
    is_read: bool = False


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications():
    """Bildirimleri listele."""
    return []


@router.get("/unread-count")
async def unread_count():
    """Okunmamış bildirim sayısı."""
    return {"count": 0}


@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: int):
    """Bildirimi okundu işaretle."""
    return {"message": f"Bildirim {notification_id} okundu"}


@router.put("/read-all")
async def mark_all_read():
    """Tüm bildirimleri okundu işaretle."""
    return {"message": "Tüm bildirimler okundu"}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int):
    """Bildirimi sil."""
    return {"message": f"Bildirim {notification_id} silindi"}
