"""
Emare SuperApp — Rate Limiting Middleware
"""
from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

# Basit in-memory rate limiter
_requests = defaultdict(list)
_lock = asyncio.Lock()

# Limitler
MAX_REQUESTS = 100  # max istek
WINDOW_SECONDS = 60  # pencere (saniye)


async def rate_limit_check(request: Request):
    """İstek limiti kontrolü."""
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.now()
    cutoff = now - timedelta(seconds=WINDOW_SECONDS)

    async with _lock:
        # Eski kayıtları temizle
        _requests[client_ip] = [
            t for t in _requests[client_ip] if t > cutoff
        ]
        if len(_requests[client_ip]) >= MAX_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Çok fazla istek — lütfen bekleyin",
            )
        _requests[client_ip].append(now)
