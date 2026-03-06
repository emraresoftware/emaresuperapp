"""
Emare SuperApp — Auth Middleware
JWT token doğrulama.
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_token
from config.settings import get_settings


security = HTTPBearer(auto_error=False)


async def verify_token(credentials: HTTPAuthorizationCredentials = None):
    """JWT token doğrulama dependency."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token gerekli",
        )
    settings = get_settings()
    try:
        payload = decode_token(
            credentials.credentials,
            settings.jwt_secret,
            settings.jwt_algorithm,
        )
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş token",
        )
