#!/bin/bash
# Emare SuperApp — Başlatma Scripti
set -e

if [ -d .venv ]; then
    source .venv/bin/activate
fi

echo "🚀 Emare SuperApp başlatılıyor — port 8080"
python3 main.py
