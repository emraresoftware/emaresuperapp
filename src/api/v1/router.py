"""
Emare SuperApp — API v1 Ana Router
47 Emare projesini yöneten merkezi gateway.
"""
from fastapi import APIRouter

api_router = APIRouter()

# ── Auth & Kullanıcı Yönetimi ──
from .auth import router as auth_router
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

from .users import router as users_router
api_router.include_router(users_router, prefix="/users", tags=["Kullanıcılar"])

# ── SuperApp Özgül Modüller ──
from .wallet import router as wallet_router
api_router.include_router(wallet_router, prefix="/wallet", tags=["Cüzdan"])

from .notifications import router as notifications_router
api_router.include_router(notifications_router, prefix="/notifications", tags=["Bildirimler"])

from .analytics import router as analytics_router
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analitik"])

# ── Emare Ekosistem Gateway ──
# Tüm 47 Emare projesine erişim: servis listesi, sağlık, proxy
from .services import router as services_router
api_router.include_router(services_router, prefix="/services", tags=["Emare Servisleri — Gateway"])
