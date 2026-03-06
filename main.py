#!/usr/bin/env python3
"""
Emare SuperApp — Ana Giriş Noktası
Tüm Emare hizmetlerini birleştiren süper uygulama platformu.
"""
import uvicorn
import sys
import os

# src klasörünü path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def main():
    """Sunucuyu başlat — ortama göre ayarlar uygulanır."""
    env = os.getenv("APP_ENV", "development")
    is_prod = env == "production"

    uvicorn.run(
        "core.app:create_app",
        factory=True,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        reload=not is_prod,          # production'da reload kapalı
        workers=int(os.getenv("WORKERS", "1" if not is_prod else "4")),
        log_level="warning" if is_prod else "info",
        access_log=not is_prod,
    )


if __name__ == "__main__":
    main()

