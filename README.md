# Emare SuperApp

> Tüm Emare hizmetlerini tek bir çatı altında birleştiren süper uygulama platformu.

## Vizyon

Emare SuperApp, kullanıcıların tüm Emare ekosistemindeki hizmetlere — finans, bulut, iletişim, yapay zeka, güvenlik, sosyal, pazar — tek bir arayüzden erişmesini sağlayan birleşik platform uygulamasıdır.

## Özellikler

| Modül | Açıklama | Durum |
|-------|----------|-------|
| **Auth** | Tek oturum açma (SSO), OAuth2, 2FA, biyometrik | 🔧 Development |
| **Wallet** | Dijital cüzdan, ödeme, kripto entegrasyonu | 📋 Planned |
| **Marketplace** | Emare ürün/servis pazaryeri | 📋 Planned |
| **Social** | Ekip içi mesajlaşma, feed, paylaşım | 📋 Planned |
| **AI Assistant** | Emare AI ile entegre akıllı asistan | 📋 Planned |
| **Notifications** | Push, email, SMS bildirim merkezi | 📋 Planned |
| **Analytics** | Kullanım analitikleri, dashboard | 📋 Planned |

## Teknoloji Stack

### Backend
- **Python 3.12+** — Ana dil
- **FastAPI** — REST + WebSocket API
- **SQLAlchemy** — ORM
- **Redis** — Cache, session, pub/sub
- **PostgreSQL** — Ana veritabanı
- **Celery** — Async task queue

### Frontend (Web)
- **React 18** / **Next.js 14** — SPA + SSR
- **TypeScript** — Tip güvenliği
- **Tailwind CSS** — Stil
- **Zustand** — State management

### Mobile
- **React Native** — Cross-platform (iOS + Android)
- **Expo** — Geliştirme workflow

### Desktop
- **Electron** / **Tauri** — Masaüstü uygulaması

### DevOps
- **Docker** + **Docker Compose**
- **Nginx** — Reverse proxy
- **GitHub Actions** — CI/CD
- **Prometheus + Grafana** — Monitoring

## Hızlı Başlangıç

```bash
# Repo klonla
cd /Users/emre/Desktop/Emare/emaresuperapp

# Backend bağımlılıkları
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Geliştirme sunucusu
python3 main.py

# Web frontend
cd web && npm install && npm run dev
```

## Dosya Yapısı

```
emaresuperapp/
├── main.py                    # Ana giriş noktası
├── requirements.txt           # Python bağımlılıkları
├── package.json              # Node.js bağımlılıkları
├── docker-compose.yml        # Container orchestration
├── .env.example              # Ortam değişkenleri şablonu
├── src/
│   ├── core/                 # Çekirdek modüller
│   │   ├── __init__.py
│   │   ├── app.py            # FastAPI app factory
│   │   ├── database.py       # DB bağlantısı
│   │   ├── security.py       # JWT, şifreleme
│   │   └── events.py         # Event bus
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Pydantic settings
│   ├── models/               # SQLAlchemy modelleri
│   ├── api/
│   │   ├── v1/               # API v1 endpointleri
│   │   └── middleware/       # Auth, CORS, rate limit
│   ├── modules/
│   │   ├── auth/             # Kimlik doğrulama
│   │   ├── wallet/           # Dijital cüzdan
│   │   ├── marketplace/      # Pazaryeri
│   │   ├── social/           # Sosyal özellikler
│   │   ├── ai_assistant/     # AI entegrasyonu
│   │   ├── notifications/    # Bildirim sistemi
│   │   └── analytics/        # Analitik
│   ├── services/             # İş mantığı servisleri
│   └── utils/                # Yardımcı fonksiyonlar
├── web/                      # React frontend
├── mobile/                   # React Native mobil
├── desktop/                  # Electron/Tauri masaüstü
├── plugins/                  # 3. parti eklenti sistemi
├── tests/                    # Test suites
├── docs/                     # Dokümantasyon
├── deploy/                   # Deployment configs
└── scripts/                  # Yardımcı scriptler
```

## Mimarî

SuperApp **modüler mikroçekirdek** mimarisi kullanır:
- Her modül bağımsız çalışabilir
- Modüller arası iletişim event bus ile sağlanır
- Plugin sistemi ile genişletilebilir
- Emare ekosistemindeki tüm projeler API üzerinden entegre olur

## Katkıda Bulunma

1. Dervişler üzerinden dev branch açılır
2. Modül bazlı PR gönderilir
3. Code review + test sonrası merge edilir

## Lisans

Emare Internal — Tüm hakları saklıdır.

---
*Emare SuperApp Dervishi tarafından yönetilir.*
