"""
Emare SuperApp — FastAPI Application Factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import pathlib
import sys

# Proje kökünü bul
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama yaşam döngüsü: başlangıç ve kapanış işlemleri."""
    # Startup
    print("🚀 Emare SuperApp başlatılıyor...")
    from .database import init_db
    await init_db()
    print("✅ Veritabanı hazır")
    yield
    # Shutdown
    print("👋 Emare SuperApp kapatılıyor...")


def create_app() -> FastAPI:
    """FastAPI uygulama fabrikası."""
    from config.settings import get_settings

    settings = get_settings()

    # Production'da API dokümantasyonu dışarıya kapalı
    docs_url = None if settings.is_production else "/docs"
    redoc_url = None if settings.is_production else "/redoc"
    openapi_url = None if settings.is_production else "/openapi.json"

    app = FastAPI(
        title="Emare SuperApp",
        description="Tüm Emare hizmetlerini birleştiren süper uygulama platformu.",
        version="0.1.0",
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan,
    )

    # ── CORS ──
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Statik dosyalar ──
    static_dir = ROOT / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # ── API Router'ları ──
    from api.v1.router import api_router
    app.include_router(api_router, prefix=settings.api_prefix)

    # ── Feedback Router ──
    try:
        import sys, pathlib
        root = pathlib.Path(__file__).resolve().parent.parent.parent
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from feedback_router import router as feedback_router
        app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
    except ImportError:
        pass  # feedback_router opsiyonel

    # ── Root endpoint ──
    @app.get("/")
    async def root():
        from services.emare_bridge import get_service_registry
        reg = get_service_registry()
        by_status: dict = {}
        for svc in reg.values():
            st = svc.get("status", "unknown")
            by_status.setdefault(st, []).append(svc["id"])
        return {
            "app": "Emare SuperApp",
            "version": "0.1.0",
            "status": "running",
            "docs": None if settings.is_production else "/docs",
            "ecosystem": {
                "total_services": len(reg),
                "production": len(by_status.get("production", [])),
                "ready": len(by_status.get("ready", [])),
                "development": len(by_status.get("development", [])),
                "planning": len(by_status.get("planning", [])),
            },
            "api_modules": [
                "auth", "users", "wallet", "notifications", "analytics",
            ],
            "gateway": {
                "services_list": f"{settings.api_prefix}/services",
                "health_all": f"{settings.api_prefix}/services/health/all",
                "proxy": f"{settings.api_prefix}/services/gateway/{{service_id}}/{{path}}",
            },
        }

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "emaresuperapp"}

    return app
