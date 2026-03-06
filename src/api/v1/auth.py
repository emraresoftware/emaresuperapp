"""
Emare SuperApp — Auth API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated

from core.database import get_db
from core.security import decode_token
from config.settings import get_settings
from modules.auth import service as auth_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


# ── Schemas ──
class RegisterRequest(BaseModel):
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    username: str  # e-posta veya kullanıcı adı
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[str] = None


# ── Dependency: mevcut kullanıcı ──
async def current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """JWT'den kullanıcı çöz; geçersizse 401 döndür."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulama gerekli",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exc
    settings = get_settings()
    try:
        payload = decode_token(token, settings.jwt_secret, settings.jwt_algorithm)
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exc
    except ValueError:
        raise credentials_exc

    user = await auth_service.get_user_by_id(db, int(user_id))
    if not user:
        raise credentials_exc
    return user


# ── Endpoints ──
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Yeni kullanıcı kaydı."""
    try:
        user = await auth_service.register_user(
            db=db,
            email=data.email,
            username=data.username,
            password=data.password,
            full_name=data.full_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Kullanıcı girişi — JWT token döndürür."""
    try:
        result = await auth_service.authenticate_user(
            db=db,
            identifier=data.username,
            password=data.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta/kullanıcı adı veya şifre hatalı",
        )
    return result


@router.get("/me", response_model=UserResponse)
async def get_me(user: dict = Depends(current_user)):
    """Mevcut kullanıcı bilgileri."""
    return user


@router.post("/logout")
async def logout():
    """Oturumu kapat (client token'ı siler)."""
    return {"message": "Başarıyla çıkış yapıldı"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(user: dict = Depends(current_user)):
    """Mevcut geçerli token ile yeni token üret."""
    settings = get_settings()
    from core.security import create_access_token
    from datetime import timedelta

    token = create_access_token(
        data={"sub": str(user["id"])},
        secret_key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expires_delta=timedelta(minutes=settings.jwt_expire_minutes),
    )
    return TokenResponse(access_token=token, expires_in=settings.jwt_expire_minutes * 60)
