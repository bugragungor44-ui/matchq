# Match Q — Çalışan yerel web uygulaması başlangıcı

## Kurulum
Python 3.10+ ile bu klasörde:
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Tarayıcıdan http://127.0.0.1:8000 adresine girin.

## Şu an çalışanlar
- Responsive ana sayfa ve üç üyelik paketinin gösterimi
- SQLite veritabanı
- `/api/status` ve `/api/plans` API uçları
- Sunucu açıkken her gün Türkiye saati 10:00'da çalışan görev

## Eksik olanlar
- Gerçek futbol verisi sağlayıcısı ve analiz/olasılık modeli
- Güvenli kullanıcı kaydı, giriş, yönetici yetkileri
- Abonelik ödeme entegrasyonu
- Bulut sunucuya dağıtım ve sürekli çalışacak zamanlayıcı

Bu prototip gerçek kupon üretmez; doğrulanmamış maç veya oran göstermez.
