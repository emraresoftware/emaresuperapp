"""Constants — uygulama sabitleri ve varsayılan yapılandırmalar."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Uygulama Bilgileri
# ---------------------------------------------------------------------------

APP_NAME: str = "Emare SuperApp"
APP_SLUG: str = "emaresuperapp"
VERSION: str = "1.0.0"
API_PREFIX: str = "/api/v1"
DESCRIPTION: str = "Emare ekosistemini tek çatı altında birleştiren süper uygulama."

# ---------------------------------------------------------------------------
# Varsayılan Sayfalama
# ---------------------------------------------------------------------------

DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100

# ---------------------------------------------------------------------------
# Token & Oturum
# ---------------------------------------------------------------------------

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 saat
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
TOKEN_ALGORITHM: str = "HS256"

# ---------------------------------------------------------------------------
# Dosya Yükleme Limitleri
# ---------------------------------------------------------------------------

MAX_UPLOAD_SIZE_MB: int = 50
ALLOWED_IMAGE_EXTENSIONS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")
ALLOWED_DOCUMENT_EXTENSIONS: tuple[str, ...] = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv")

# ---------------------------------------------------------------------------
# Para Birimleri
# ---------------------------------------------------------------------------

DEFAULT_CURRENCY: str = "TRY"
SUPPORTED_CURRENCIES: tuple[str, ...] = ("TRY", "USD", "EUR", "GBP")

# ---------------------------------------------------------------------------
# Bildirim Türleri
# ---------------------------------------------------------------------------

NOTIFICATION_TYPES: tuple[str, ...] = ("info", "warning", "success", "error")

# ---------------------------------------------------------------------------
# Emare Ekosistem Servisleri (varsayılan URL'ler)
# ---------------------------------------------------------------------------

DEFAULT_SERVICE_URLS: dict[str, str] = {
    "cloud": "http://localhost:8001",
    "asistan": "http://localhost:8002",
    "flow": "http://localhost:8003",
    "database": "http://localhost:8004",
    "finance": "http://localhost:8005",
    "hub": "http://localhost:8006",
}

# ---------------------------------------------------------------------------
# AI Sağlayıcılar
# ---------------------------------------------------------------------------

DEFAULT_AI_PROVIDER: str = "openai"
SUPPORTED_AI_PROVIDERS: tuple[str, ...] = ("openai", "gemini")
DEFAULT_AI_MODEL: str = "gpt-4o"
DEFAULT_AI_TEMPERATURE: float = 0.7
DEFAULT_AI_MAX_TOKENS: int = 2048

# ---------------------------------------------------------------------------
# Rate Limiting
# ---------------------------------------------------------------------------

RATE_LIMIT_PER_MINUTE: int = 60
RATE_LIMIT_PER_HOUR: int = 1000

# ---------------------------------------------------------------------------
# Ortam Sabitleri
# ---------------------------------------------------------------------------

ENV_DEVELOPMENT: str = "development"
ENV_STAGING: str = "staging"
ENV_PRODUCTION: str = "production"
