# Emare SuperApp — API Dokümantasyonu

## Base URL
- **Development**: `http://localhost:8080`
- **Production**: `https://superapp.emare.com`

## Auth Header
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Auth
| Metod | Yol | Açıklama |
|-------|-----|----------|
| POST | /api/v1/auth/register | Yeni kullanıcı kaydı |
| POST | /api/v1/auth/login | Giriş (JWT al) |
| GET | /api/v1/auth/me | Mevcut kullanıcı |
| POST | /api/v1/auth/logout | Çıkış |
| POST | /api/v1/auth/refresh | Token yenile |

### Wallet
| Metod | Yol | Açıklama |
|-------|-----|----------|
| GET | /api/v1/wallet/balance | Bakiye sorgula |
| POST | /api/v1/wallet/deposit | Para yatır |
| POST | /api/v1/wallet/withdraw | Para çek |
| POST | /api/v1/wallet/transfer | Transfer |
| GET | /api/v1/wallet/transactions | İşlem geçmişi |

### Marketplace
| Metod | Yol | Açıklama |
|-------|-----|----------|
| GET | /api/v1/marketplace/products | Ürün listesi |
| GET | /api/v1/marketplace/products/:id | Ürün detayı |
| POST | /api/v1/marketplace/products | Ürün ekle |
| GET | /api/v1/marketplace/categories | Kategoriler |
| POST | /api/v1/marketplace/products/:id/purchase | Satın al |

### Social
| Metod | Yol | Açıklama |
|-------|-----|----------|
| GET | /api/v1/social/feed | Akış |
| POST | /api/v1/social/posts | Gönderi paylaş |
| POST | /api/v1/social/posts/:id/like | Beğen |
| GET | /api/v1/social/messages | Mesajlar |
| POST | /api/v1/social/messages | Mesaj gönder |

### Notifications
| Metod | Yol | Açıklama |
|-------|-----|----------|
| GET | /api/v1/notifications/ | Bildirimler |
| GET | /api/v1/notifications/unread-count | Okunmamış sayı |
| PUT | /api/v1/notifications/:id/read | Okundu işaretle |
| PUT | /api/v1/notifications/read-all | Hepsini okundu yap |

### Analytics
| Metod | Yol | Açıklama |
|-------|-----|----------|
| GET | /api/v1/analytics/overview | Genel özet |
| GET | /api/v1/analytics/modules | Modül kullanımı |
| GET | /api/v1/analytics/users/growth | Kullanıcı büyümesi |
| GET | /api/v1/analytics/revenue | Gelir istatistikleri |

## Swagger UI
Çalışırken: `http://localhost:8080/docs`
