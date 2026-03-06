"""
Emare SuperApp — Güvenlik Modülü
JWT token üretimi, şifre hashleme, OAuth2.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext


# Şifre hashleme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Şifreyi hashle."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Şifreyi doğrula."""
    return pwd_context.verify(plain, hashed)


def create_access_token(
    data: dict,
    secret_key: str,
    algorithm: str = "HS256",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """JWT access token oluştur."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithm: str = "HS256") -> dict:
    """JWT token çöz."""
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        raise ValueError("Geçersiz veya süresi dolmuş token")
