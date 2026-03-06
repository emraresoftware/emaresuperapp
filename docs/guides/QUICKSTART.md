# Emare SuperApp — Hızlı Başlangıç Kılavuzu

## 1. Gereksinimler
- Python 3.12+
- Node.js 20+ (web frontend için)
- Redis (opsiyonel, cache için)
- PostgreSQL (production için; development'ta SQLite kullanılır)

## 2. Kurulum

```bash
cd /Users/emre/Desktop/Emare/emaresuperapp
chmod +x setup.sh
./setup.sh
```

veya manuel:

```bash
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
pip install -r requirements.txt
```

## 3. Çalıştırma

```bash
source .venv/bin/activate
python3 main.py
```

API: http://localhost:8080
Docs: http://localhost:8080/docs

## 4. Docker ile

```bash
docker-compose up -d
```

## 5. Web Frontend

```bash
cd web
npm install
npm run dev
```

http://localhost:3000

## 6. Testler

```bash
pytest tests/ -v
```

## 7. Yapı
- `src/` — Backend kaynak kodu
- `web/` — React frontend
- `mobile/` — React Native mobil uygulama
- `docs/` — Dokümantasyon
- `tests/` — Testler
