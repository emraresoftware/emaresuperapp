# Emare SuperApp — Mimari Doküman

## Genel Bakış

SuperApp, **modüler mikroçekirdek** mimarisi üzerine kuruludur:

```
┌──────────────────────────────────────────────┐
│              Emare SuperApp                   │
├──────────────────────────────────────────────┤
│  Web (React)  │  Mobile (RN)  │  Desktop     │
├──────────────────────────────────────────────┤
│               API Gateway (FastAPI)           │
├───────┬───────┬────────┬──────┬──────────────┤
│ Auth  │Wallet │Market  │Social│ AI Assistant  │
│       │       │ place  │      │               │
├───────┴───────┴────────┴──────┴──────────────┤
│            Core Layer                         │
│  Database │ Cache │ Events │ Security         │
├──────────────────────────────────────────────┤
│  PostgreSQL  │  Redis  │  File Storage        │
└──────────────────────────────────────────────┘
```

## Katmanlar

### 1. Sunum Katmanı (Frontend)
- **Web**: React + Next.js, SSR destekli
- **Mobile**: React Native, iOS + Android
- **Desktop**: Electron/Tauri

### 2. API Katmanı
- FastAPI ile RESTful + WebSocket
- JWT tabanlı authentication
- Rate limiting, CORS, logging middleware
- OpenAPI (Swagger) otomatik dokümantasyon

### 3. Modül Katmanı
Her modül bağımsız bir mini-uygulama gibi çalışır:
- **Auth**: SSO, OAuth2, 2FA
- **Wallet**: Dijital cüzdan, ödeme
- **Marketplace**: Emare ürün/servis pazaryeri
- **Social**: Feed, mesajlaşma, paylaşım
- **AI Assistant**: Gemini/OpenAI entegrasyonu
- **Notifications**: Push, email, SMS, in-app
- **Analytics**: Kullanım metrikleri, dashboard

### 4. Çekirdek Katman (Core)
- **Database**: SQLAlchemy async, PostgreSQL/SQLite
- **Cache**: Redis ile session + veri cache
- **Events**: Async event bus (modüller arası)
- **Security**: JWT, bcrypt, rate limiting

### 5. Altyapı
- Docker + Docker Compose
- Nginx reverse proxy
- Prometheus + Grafana monitoring
- GitHub Actions CI/CD

## Emare Ekosistem Entegrasyonu

SuperApp, **Emare Bridge** servisi üzerinden diğer tüm Emare projelerine bağlanır:

| Proje | Entegrasyon |
|-------|-------------|
| EmareCloud | Sunucu/container yönetimi |
| Emare Asistan | AI müşteri hizmetleri |
| Emare Finance | Finans modülleri |
| EmareHup | Git/proje yönetimi |
| EmareSiber | Güvenlik taramaları |

## Veri Akışı

```
Kullanıcı İsteği
    → API Gateway (auth + rate limit)
    → Router → Modül API Endpoint
    → Service Layer (iş mantığı)
    → Model Layer (DB işlemleri)
    → Event Bus (diğer modüllere bildirim)
    → Response
```
