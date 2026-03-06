"""Auth Service — kullanıcı kayıt, giriş ve oturum yönetimi."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password, create_access_token
from config.settings import get_settings


# ---------------------------------------------------------------------------
# Kullanıcı Kayıt
# ---------------------------------------------------------------------------

async def register_user(
    db: AsyncSession,
    email: str,
    username: str,
    password: str,
    full_name: str | None = None,
) -> dict[str, Any]:
    """Yeni kullanıcı kaydı oluşturur; e-posta veya kullanıcı adı alınmışsa ValueError fırlatır."""
    from models.user import User

    # Benzersizlik kontrolü
    existing = await db.scalar(
        select(User).where(
            (User.email == email) | (User.username == username)
        )
    )
    if existing:
        if existing.email == email:
            raise ValueError("Bu e-posta adresi zaten kullanılıyor")
        raise ValueError("Bu kullanıcı adı zaten alınmış")

    user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
        full_name=full_name,
        is_active=True,
    )
    db.add(user)
    await db.flush()   # id üret
    await db.refresh(user)
    return _user_dict(user)


# ---------------------------------------------------------------------------
# Kimlik Doğrulama
# ---------------------------------------------------------------------------

async def authenticate_user(
    db: AsyncSession,
    identifier: str,   # e-posta veya kullanıcı adı
    password: str,
) -> dict[str, Any] | None:
    """Kullanıcı adı/e-posta ve şifre ile doğrulama; başarılıysa token + kullanıcı döndürür."""
    from models.user import User

    user = await db.scalar(
        select(User).where(
            (User.email == identifier) | (User.username == identifier)
        )
    )
    if user is None or not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        raise ValueError("Hesap devre dışı")  

    settings = get_settings()
    token = create_access_token(
        data={"sub": str(user.id)},
        secret_key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expires_delta=timedelta(minutes=settings.jwt_expire_minutes),
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.jwt_expire_minutes * 60,
        "user": _user_dict(user),
    }


# ---------------------------------------------------------------------------
# Mevcut Kullanıcı Bilgisi
# ---------------------------------------------------------------------------

async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> dict[str, Any] | None:
    """ID ile kullanıcı bilgisini döndürür."""
    from models.user import User

    user = await db.scalar(select(User).where(User.id == user_id))
    return _user_dict(user) if user else None


# ---------------------------------------------------------------------------
# Yardımcı
# ---------------------------------------------------------------------------

def _user_dict(user: Any) -> dict[str, Any]:
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "avatar_url": getattr(user, "avatar_url", None),
        "is_active": user.is_active,
        "is_superuser": getattr(user, "is_superuser", False),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
