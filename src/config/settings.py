"""
Emare SuperApp — Uygulama Ayarları
Pydantic Settings ile tip güvenlikli yapılandırma.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
import pathlib


class Settings(BaseSettings):
    """Uygulama yapılandırması — .env dosyasından okunur."""

    # Genel
    app_name: str = "EmareSuperApp"
    app_env: str = "development"
    debug: bool = False          # Production'da kesinlikle False olmalı
    secret_key: str = "change-me-in-production"  # .env'den override edilmeli!
    api_prefix: str = "/api/v1"

    # Sunucu
    host: str = "0.0.0.0"
    port: int = 8080

    # Veritabanı
    database_url: str = "sqlite+aiosqlite:///./data/superapp.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret: str = "superapp-jwt-secret-change-me"  # .env'den override edilmeli!
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60  # Varsayılan 1 saat; production'da kısa tut

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""

    # AI
    gemini_api_key: str = ""
    openai_api_key: str = ""

    # Emare Ekosistem
    emare_hub_url: str = "http://localhost:5555"
    emare_cloud_url: str = "http://77.92.152.3:5000"
    emare_asistan_url: str = "http://77.92.152.3:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    model_config = {
        "env_file": str(pathlib.Path(__file__).resolve().parent.parent.parent / ".env"),
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",   # .env'deki bilinmeyen alanları sessizce atla
    }


@lru_cache()
def get_settings() -> Settings:
    """Singleton settings instance."""
    return Settings()
