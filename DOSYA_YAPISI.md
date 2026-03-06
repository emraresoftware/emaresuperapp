# Emare SuperApp — Dosya Yapısı

```
emaresuperapp/
│
├── main.py                          # Ana giriş noktası (uvicorn launcher)
├── README.md                        # Proje açıklaması
├── DOSYA_YAPISI.md                  # Bu dosya
├── EMARE_ANAYASA.md                 # Emare anayasa kopyası
├── EMARE_ORTAK_HAFIZA.md            # Ortak hafıza bağlantısı
├── requirements.txt                 # Python bağımlılıkları
├── package.json                     # Node.js meta (web + mobile)
├── docker-compose.yml               # Docker orchestration
├── Dockerfile                       # Backend container
├── .env.example                     # Ortam değişkenleri şablonu
├── setup.sh                         # Tek adımda kurulum
├── start.sh                         # Çalıştırma scripti
│
├── src/                             # ═══ BACKEND KAYNAK KODU ═══
│   ├── __init__.py
│   ├── core/                        # Çekirdek sistem
│   │   ├── __init__.py
│   │   ├── app.py                   # FastAPI app factory
│   │   ├── database.py              # SQLAlchemy engine + session
│   │   ├── security.py              # JWT, bcrypt, OAuth2
│   │   ├── events.py                # Event bus (pub/sub)
│   │   ├── cache.py                 # Redis cache wrapper
│   │   └── exceptions.py            # Özel exception sınıfları
│   │
│   ├── config/                      # Yapılandırma
│   │   ├── __init__.py
│   │   └── settings.py              # Pydantic BaseSettings
│   │
│   ├── models/                      # Veritabanı modelleri
│   │   ├── __init__.py
│   │   ├── user.py                  # User, Role, Permission
│   │   ├── wallet.py                # Wallet, Transaction
│   │   ├── product.py               # Product, Category
│   │   ├── notification.py          # Notification, Channel
│   │   └── base.py                  # Base model mixin
│   │
│   ├── api/                         # API katmanı
│   │   ├── __init__.py
│   │   ├── v1/                      # API v1
│   │   │   ├── __init__.py
│   │   │   ├── router.py            # Ana router (tüm modüller)
│   │   │   ├── auth.py              # /api/v1/auth/*
│   │   │   ├── users.py             # /api/v1/users/*
│   │   │   ├── wallet.py            # /api/v1/wallet/*
│   │   │   ├── marketplace.py       # /api/v1/marketplace/*
│   │   │   ├── social.py            # /api/v1/social/*
│   │   │   ├── notifications.py     # /api/v1/notifications/*
│   │   │   └── analytics.py         # /api/v1/analytics/*
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth_middleware.py    # JWT doğrulama
│   │       ├── cors.py              # CORS ayarları
│   │       ├── rate_limit.py        # Rate limiting
│   │       └── logging_mw.py        # İstek/yanıt loglama
│   │
│   ├── modules/                     # ═══ İŞ MODÜLLER İ ═══
│   │   ├── auth/                    # Kimlik doğrulama modülü
│   │   │   ├── __init__.py
│   │   │   ├── service.py           # Auth business logic
│   │   │   ├── schemas.py           # Pydantic schemas
│   │   │   └── utils.py             # Token, hash helpers
│   │   ├── wallet/                  # Dijital cüzdan
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   ├── marketplace/             # Pazaryeri
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   ├── social/                  # Sosyal özellikler
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   ├── ai_assistant/            # AI entegrasyonu
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   ├── notifications/           # Bildirim sistemi
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   └── analytics/               # Analitik modülü
│   │       ├── __init__.py
│   │       ├── service.py
│   │       └── schemas.py
│   │
│   ├── services/                    # Paylaşılan servisler
│   │   ├── __init__.py
│   │   ├── email_service.py         # Email gönderimi
│   │   ├── sms_service.py           # SMS gönderimi
│   │   ├── push_service.py          # Push notification
│   │   ├── storage_service.py       # Dosya depolama
│   │   └── emare_bridge.py          # Diğer Emare projelerine köprü
│   │
│   └── utils/                       # Yardımcı araçlar
│       ├── __init__.py
│       ├── helpers.py               # Genel yardımcılar
│       ├── validators.py            # Doğrulama fonksiyonları
│       └── constants.py             # Sabitler
│
├── web/                             # ═══ WEB FRONTEND ═══
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── public/
│   │   ├── favicon.ico
│   │   └── manifest.json
│   └── src/
│       ├── components/              # React bileşenleri
│       ├── pages/                   # Next.js sayfaları
│       ├── styles/                  # CSS / Tailwind
│       ├── hooks/                   # Custom React hooks
│       ├── store/                   # Zustand state
│       └── utils/                   # Frontend yardımcıları
│
├── mobile/                          # ═══ MOBİL UYGULAMA ═══
│   ├── ios/                         # iOS native config
│   ├── android/                     # Android native config
│   └── shared/                      # Paylaşılan RN kod
│
├── desktop/                         # ═══ MASAÜSTÜ ═══
│   └── src/                         # Electron/Tauri kaynak
│
├── plugins/                         # ═══ EKLENTİ SİSTEMİ ═══
│   └── README.md                    # Plugin geliştirme kılavuzu
│
├── templates/                       # Jinja2 / HTML şablonlar
├── static/                          # Statik dosyalar
│   ├── css/
│   ├── js/
│   └── img/
│
├── tests/                           # ═══ TESTLER ═══
│   ├── unit/                        # Birim testler
│   ├── integration/                 # Entegrasyon testleri
│   └── e2e/                         # Uçtan uca testler
│
├── docs/                            # ═══ DOKÜMANTASYON ═══
│   ├── api/                         # OpenAPI / Swagger
│   ├── architecture/                # Mimari dokümanları
│   └── guides/                      # Kullanım kılavuzları
│
├── scripts/                         # Yardımcı scriptler
├── deploy/                          # Deployment yapılandırması
├── data/                            # Yerel veri dosyaları
├── web_dizayn/                      # Emare Asistan web tasarımı
└── EMARE_ORTAK_CALISMA/            # Ortak çalışma alanı
```
