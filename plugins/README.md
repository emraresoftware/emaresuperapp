# Emare SuperApp — Plugin Sistemi

## Nasıl Plugin Geliştirilir?

Emare SuperApp modüler bir mimariye sahiptir. Yeni özellikler plugin olarak eklenebilir.

### Plugin Yapısı

```
plugins/
└── my_plugin/
    ├── __init__.py      # Plugin meta + register fonksiyonu
    ├── routes.py        # FastAPI router
    ├── service.py       # İş mantığı
    └── models.py        # DB modelleri (opsiyonel)
```

### Minimal Plugin Örneği

```python
# plugins/my_plugin/__init__.py
from fastapi import APIRouter

PLUGIN_INFO = {
    "name": "My Plugin",
    "version": "1.0.0",
    "author": "Emare",
}

router = APIRouter(prefix="/my-plugin", tags=["My Plugin"])

@router.get("/")
async def hello():
    return {"message": "Merhaba, ben bir plugin!"}


def register(app):
    """Plugin'i uygulamaya kaydet."""
    app.include_router(router)
```

### Kurallar
1. Her plugin kendi klasöründe yaşar
2. `register(app)` fonksiyonu zorunludur
3. Plugin kendi DB tablolarını oluşturabilir (Alembic migration ile)
4. Diğer modüllere event bus üzerinden erişebilir
5. Plugin ayarları `.env` dosyasında `PLUGIN_` prefix'i ile tanımlanır
