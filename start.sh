#!/bin/bash
# Emare SuperApp — Başlatma Scripti
set -e

cd "$(dirname "$0")"

# .env.development varsa yükle
if [ -f .env.development ]; then
    export $(grep -v '^#' .env.development | xargs)
fi

# Varsayılanlar
export APP_ENV="${APP_ENV:-development}"
export DATABASE_URL="${DATABASE_URL:-sqlite+aiosqlite:///./emare_dev.db}"
export PYTHONPATH="${PYTHONPATH:-$(pwd)/src}"

if [ -d .venv ]; then
    source .venv/bin/activate
fi

echo "🚀 Emare SuperApp başlatılıyor (${APP_ENV}) — http://localhost:8000"
echo "📖 Swagger UI: http://localhost:8000/docs"
echo "🌐 Servisler:  http://localhost:8000/api/v1/services"

uvicorn src.core.app:create_app --factory \
    --reload \
    --port 8000 \
    --host 0.0.0.0 \
    --log-level info
