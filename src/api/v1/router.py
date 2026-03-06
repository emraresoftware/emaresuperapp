"""
Emare SuperApp — API v1 Ana Router
Tüm modül router'larını birleştirir.
"""
from fastapi import APIRouter

api_router = APIRouter()

# ── Auth ──
from .auth import router as auth_router
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# ── Users ──
from .users import router as users_router
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# ── Wallet ──
from .wallet import router as wallet_router
api_router.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])

# ── Marketplace ──
from .marketplace import router as marketplace_router
api_router.include_router(marketplace_router, prefix="/marketplace", tags=["Marketplace"])

# ── Social ──
from .social import router as social_router
api_router.include_router(social_router, prefix="/social", tags=["Social"])

# ── Notifications ──
from .notifications import router as notifications_router
api_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])

# ── Analytics ──
from .analytics import router as analytics_router
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
