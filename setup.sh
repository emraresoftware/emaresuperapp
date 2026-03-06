#!/bin/bash
# ═══════════════════════════════════════
# Emare SuperApp — Kurulum Scripti
# ═══════════════════════════════════════
set -e

echo "🚀 Emare SuperApp kurulumu başlıyor..."

# .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env dosyası oluşturuldu"
fi

# Python venv
if [ ! -d .venv ]; then
    python3 -m venv .venv
    echo "✅ Python sanal ortam oluşturuldu"
fi

source .venv/bin/activate

# Bağımlılıklar
pip install -r requirements.txt
echo "✅ Python bağımlılıkları kuruldu"

# Data klasörü
mkdir -p data
echo "✅ Data klasörü hazır"

# Web frontend
if [ -f web/package.json ]; then
    cd web && npm install && cd ..
    echo "✅ Web bağımlılıkları kuruldu"
fi

echo ""
echo "═══════════════════════════════════════"
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Çalıştırmak için:"
echo "  source .venv/bin/activate"
echo "  python3 main.py"
echo ""
echo "Veya Docker ile:"
echo "  docker-compose up -d"
echo "═══════════════════════════════════════"
