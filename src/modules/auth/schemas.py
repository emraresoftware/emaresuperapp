"""Auth Schemas — kimlik doğrulama Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Kayıt
# ---------------------------------------------------------------------------

class RegisterSchema(BaseModel):
    """Yeni kullanıcı kayıt isteği."""

    email: EmailStr
    password: str = Field(..., min_length=8, description="En az 8 karakter")
    full_name: str | None = Field(None, max_length=120)


# ---------------------------------------------------------------------------
# Giriş
# ---------------------------------------------------------------------------

class LoginSchema(BaseModel):
    """Kullanıcı giriş isteği."""

    email: EmailStr
    password: str


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

class TokenSchema(BaseModel):
    """JWT erişim tokenı yanıtı."""

    access_token: str
    token_type: str = "bearer"


# ---------------------------------------------------------------------------
# Kullanıcı
# ---------------------------------------------------------------------------

class UserSchema(BaseModel):
    """Kullanıcı bilgi yanıtı."""

    id: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
