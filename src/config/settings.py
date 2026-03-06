"""
Emare SuperApp — Uygulama Ayarları
Pydantic Settings ile tip güvenlikli yapılandırma.
47 Emare projesi bu settings üzerinden bağlanır.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
import pathlib


class Settings(BaseSettings):
    """Uygulama yapılandırması — .env dosyasından okunur."""

    # ── Genel ────────────────────────────────────────────────────────────
    app_name: str = "EmareSuperApp"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    api_prefix: str = "/api/v1"
    workers: int = 1

    # ── Sunucu ───────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8080

    # ── Veritabanı ───────────────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./data/superapp.db"

    # ── Redis ────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── JWT ──────────────────────────────────────────────────────────────
    jwt_secret: str = "superapp-jwt-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # ── CORS ─────────────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    # ── Email ────────────────────────────────────────────────────────────
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""

    # ── AI API Anahtarları ───────────────────────────────────────────────
    gemini_api_key: str = ""
    openai_api_key: str = ""

    # ════════════════════════════════════════════════════════════════════
    # EMARE EKOSİSTEM SERVİS URL'LERİ
    # projects.json'daki 47 projenin erişim adresleri
    # ════════════════════════════════════════════════════════════════════

    # ── PRODUCTION servisler (canlı) ─────────────────────────────────────
    # Emare Asistan — WhatsApp/TG/IG AI müşteri hizmetleri (77.92.152.3:8000)
    emare_asistan_url: str = "http://77.92.152.3:8000"
    # EmareCloud — Sunucu yönetim paneli (185.189.54.104:80)
    emare_cloud_url: str = "http://185.189.54.104"
    # Emare Finance — SaaS POS + e-Fatura (77.92.152.3:3000)
    emare_finance_url: str = "http://77.92.152.3:3000"
    # Emare Makale — Otomatik TR makale üretimi
    emare_makale_url: str = "http://localhost:5000"
    # Emare Team — Kanban + görev yönetimi
    emare_team_url: str = "http://localhost:5001"
    # Emare Dashboard — Ekosistem kontrol paneli
    emare_dashboard_url: str = "http://localhost:5050"
    # Emare Code — AI kod üretici
    emare_code_url: str = "http://localhost:8010"

    # ── READY servisler (deploy edilebilir) ───────────────────────────────
    # EmareDesk — WebSocket uzak masaüstü (RemoteView)
    emare_desk_url: str = "http://localhost:8765"
    # Hive Coordinator — 9B düğümlü yazılım ekibi koordinasyonu
    emare_hive_url: str = "http://localhost:8001"
    # Emare Katip — Proje tarayıcı + raporlayıcı
    emare_katip_url: str = "http://localhost:8020"
    # Emare GitHub — Toplu GitHub push aracı
    emare_github_url: str = "http://localhost:8030"

    # ── DEVELOPMENT servisler ─────────────────────────────────────────────
    # Emare POS — Restoran adisyon sistemi
    emare_pos_url: str = "http://localhost:8082"
    # Emare Log — ISS CRM+ERP+NOC (MikroTik, 5651 log)
    emare_log_url: str = "http://localhost:8083"
    # Emare Aplince Desk — Teknik servis yönetimi
    emare_aplincedesk_url: str = "http://localhost:8084"
    # Emare CC — Çağrı merkezi (Asterisk, AI transkript)
    emare_cc_url: str = "http://localhost:3080"
    # EmareSetup — AI yazılım fabrikası CLI
    emare_setup_url: str = "http://localhost:8000"
    # EmareHup — DevM otonom geliştirme orchestrator
    emare_hup_url: str = "http://localhost:5555"
    # Emare Flow — n8n benzeri görsel iş akışı
    emare_flow_url: str = "http://localhost:5173"
    # Emare Intranet — İç iletişim platformu
    emare_intranet_url: str = "http://localhost:8200"
    # Emare Crypto — Kripto/blockchain entegrasyonu
    emare_crypto_url: str = "http://localhost:8300"
    # Emare Pazar — Ürün/hizmet pazaryeri
    emare_pazar_url: str = "http://localhost:8500"
    # Emare AI Music — AI müzik üretimi
    emare_aimusic_url: str = "http://localhost:8700"
    # Emare Webdizayn — UI/UX ajans yönetimi
    emare_webdizayn_url: str = "http://localhost:8900"
    # Emare AI — Self-hosted LLM (LLaMA/Mistral)
    emare_ai_url: str = "http://localhost:8888"
    # Emare VS Code Asistan — Ayar senkronizasyonu
    emare_vscodeasistan_url: str = "http://localhost:8040"
    # Emare Ads — AI browser extension backend
    emare_ads_url: str = "http://localhost:8050"
    # Emare Ulak — Chat izleyici WebSocket server
    emare_ulak_url: str = "http://localhost:8060"
    # Emare Siber — Pentest + siber güvenlik
    emare_siber_url: str = "http://localhost:8070"
    # EmareBot — Trendyol Kozmopol bot (masaüstü, API yoksa boş)
    emare_bot_url: str = ""
    # Emare Hosting — Hosting altyapısı
    emare_hosting_url: str = "http://localhost:8110"
    # Emare Free — Ücretsiz hizmet toplayıcı
    emare_free_url: str = ""
    # SiberEmare (multi-agent pentest)
    emare_siberemare_url: str = "http://localhost:8120"
    # ZeusDB / EmareOracle
    emare_oracle_url: str = "http://localhost:7777"

    # ── Eski / genel URL ─────────────────────────────────────────────────
    emare_hub_url: str = "http://localhost:5555"  # EmareHup ile aynı

    # ════════════════════════════════════════════════════════════════════

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
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Singleton settings instance."""
    return Settings()
