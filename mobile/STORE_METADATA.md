# Emare SuperApp — App Store & Google Play Metadata

## App Store (iOS)

**App Adı:** Emare SuperApp
**Subtitle:** Finans, AI, Bulut — Hepsi Cebinde
**Bundle ID:** com.emare.superapp
**SKU:** emare-superapp-ios

**Kategori:** Finance (Ana), Productivity (İkincil)
**Yaş Sınırı:** 4+

### Açıklama (Türkçe)
Emare SuperApp, 47'den fazla Emare servisini tek uygulamada bir araya getirir.

💳 **Cüzdan & Finans** — Anlık bakiye takibi, hızlı transfer
🤖 **AI Asistan** — Yapay zeka destekli kişisel asistan
☁️ **Bulut Depolama** — Dosyalarınız her zaman yanınızda
📊 **Analitik** — Harcama ve kullanım istatistikleri
🔔 **Bildirimler** — Anlık, önemli hiçbir şeyi kaçırmayın
🌐 **Ekosistem** — Tüm Emare servislerine tek noktadan erişim

### Anahtar Kelimeler (100 karakter)
finans,cüzdan,AI,asistan,bulut,analitik,superapp,emare,ödeme,transfer

### Destek URL
https://emare.app/support

### Pazarlama URL
https://emare.app

### Gizlilik Politikası URL
https://emare.app/privacy

---

## Google Play (Android)

**Uygulama Adı:** Emare SuperApp
**Package:** com.emare.superapp
**Kategori:** Finance
**İçerik Derecelendirmesi:** Everyone

### Kısa Açıklama (80 karakter)
47+ Emare servisi tek uygulamada — finans, AI, bulut ve daha fazlası

### Tam Açıklama
(App Store açıklamasıyla aynı)

### Etiketler
finans, cüzdan, AI asistan, bulut, süper uygulama

---

## Release Notları (v1.0.0)

### Türkçe
• İlk yayın
• 47 Emare servisi entegrasyonu
• Cüzdan ve anlık bakiye takibi
• AI Asistan erişimi
• Anlık bildirimler

---

## Gerekli Varlıklar (assets/)

| Dosya | Boyut | Platform |
|---|---|---|
| icon.png | 1024×1024 | iOS + Android |
| splash.png | 1284×2778 | iOS |
| adaptive-icon.png | 1024×1024 | Android |
| feature-graphic.png | 1024×500 | Google Play |
| screenshots/ios/*.png | 1242×2688 | App Store |
| screenshots/android/*.png | 1080×1920 | Google Play |
| notification-icon.png | 96×96 | Android |

---

## EAS Kurulum Adımları

```bash
# 1. EAS CLI kur
npm install -g eas-cli

# 2. Expo hesabına giriş
eas login

# 3. Proje bağla
cd mobile && eas init --id emaresuperapp-project-id

# 4. Sertifikaları oluştur (otomatik)
eas credentials

# 5. Preview build (test için)
npm run build:preview

# 6. Production build
npm run build:all

# 7. Store'a gönder
npm run submit:all
```

## Apple Developer Hesabı Gereksinimleri
- Apple Developer Program üyeliği ($99/yıl)
- App Store Connect'te uygulama oluşturulmuş olmalı
- `ascAppId` değeri eas.json'a girilmeli
- Team ID: Apple Developer Portal > Membership

## Google Play Gereksinimleri  
- Google Play Console hesabı ($25 tek seferlik)
- Service account JSON: Play Console > API access > Service accounts
- `google-play-service-account.json` dosyası mobile/ klasörüne koyulmalı (gitignore'da)
