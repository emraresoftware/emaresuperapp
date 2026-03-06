"""Social Service — sosyal etkileşim işlemleri."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


# ---------------------------------------------------------------------------
# Gönderi Oluştur
# ---------------------------------------------------------------------------

async def create_post(
    user_id: str,
    content: str,
    media_urls: list[str] | None = None,
) -> dict[str, Any]:
    """Yeni sosyal gönderi oluşturur.

    Returns:
        Oluşturulan gönderi bilgileri.
    """
    post_id = str(uuid4())

    # TODO: Veritabanına gönderi kaydı ekle
    return {
        "id": post_id,
        "user_id": user_id,
        "content": content,
        "media_urls": media_urls or [],
        "likes_count": 0,
        "comments_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Akış (Feed)
# ---------------------------------------------------------------------------

async def get_feed(
    user_id: str,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Kullanıcının sosyal akışını döndürür.

    Takip edilen kişilerin gönderilerini zamana göre sıralar.
    """
    # TODO: Takip listesine göre gönderileri sorgula
    return {
        "items": [],
        "page": page,
        "page_size": page_size,
        "total": 0,
    }


# ---------------------------------------------------------------------------
# Beğeni
# ---------------------------------------------------------------------------

async def like_post(user_id: str, post_id: str) -> bool:
    """Gönderiyi beğenir.

    Returns:
        Başarılıysa ``True``.
    """
    # TODO: Veritabanında beğeni kaydı oluştur (idempotent)
    return True


async def unlike_post(user_id: str, post_id: str) -> bool:
    """Gönderi beğenisini kaldırır."""
    # TODO: Veritabanından beğeni kaydını sil
    return True


# ---------------------------------------------------------------------------
# Yorum
# ---------------------------------------------------------------------------

async def add_comment(
    user_id: str,
    post_id: str,
    content: str,
) -> dict[str, Any]:
    """Gönderiye yorum ekler.

    Returns:
        Oluşturulan yorum bilgileri.
    """
    comment_id = str(uuid4())

    # TODO: Veritabanına yorum kaydı ekle
    return {
        "id": comment_id,
        "user_id": user_id,
        "post_id": post_id,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Takip
# ---------------------------------------------------------------------------

async def follow_user(follower_id: str, target_id: str) -> bool:
    """Hedef kullanıcıyı takip eder.

    Returns:
        Başarılıysa ``True``.
    """
    if follower_id == target_id:
        raise ValueError("Kendinizi takip edemezsiniz.")

    # TODO: Veritabanında takip kaydı oluştur
    return True


async def unfollow_user(follower_id: str, target_id: str) -> bool:
    """Hedef kullanıcıyı takipten çıkarır."""
    # TODO: Veritabanından takip kaydını sil
    return True


# ---------------------------------------------------------------------------
# Profil
# ---------------------------------------------------------------------------

async def get_profile(user_id: str) -> dict[str, Any] | None:
    """Kullanıcının sosyal profil bilgilerini döndürür."""
    # TODO: Veritabanından profil bilgisi çek
    return None
