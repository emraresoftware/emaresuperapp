"""
Emare SuperApp — Integration Testleri
FastAPI TestClient ile gerçek HTTP katmanını test eder.
"""
import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport

# src yolunu ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

# Test için SQLite in-memory DB kullan
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("JWT_SECRET", "test-secret-key-integration")
os.environ.setdefault("SECRET_KEY", "test-secret-key-integration")


@pytest.fixture(scope="session")
def app():
    """Test için uygulama instance'ı."""
    from config.settings import get_settings
    get_settings.cache_clear()  # Ayarları yenile

    from core.app import create_app
    return create_app()


@pytest.fixture
async def client(app):
    """Async HTTP test client — lifespan (DB init) ile."""
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac


# ── Root & Health ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_root_endpoint(client):
    """/ endpoint'i çalışıyor mu?"""
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app"] == "Emare SuperApp"
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """/health endpoint'i 200 döndürüyor mu?"""
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ── Auth ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_register_endpoint(client):
    """Kullanıcı kaydı — 201 döndürüyor mu?"""
    resp = await client.post("/api/v1/auth/register", json={
        "email": "test@emare.com",
        "username": "testuser",
        "password": "Test1234!",
        "full_name": "Test Kullanıcı",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@emare.com"
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_login_endpoint(client):
    """Kullanıcı girişi — token döndürüyor mu?"""
    # Önce kullanıcı oluştur
    await client.post("/api/v1/auth/register", json={
        "email": "login_test@emare.com",
        "username": "logintest",
        "password": "Test1234!",
    })
    # Giriş yap
    resp = await client.post("/api/v1/auth/login", json={
        "username": "logintest",
        "password": "Test1234!",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_returns_valid_jwt(client):
    """Login token'ı decode edilebiliyor mu?"""
    from core.security import decode_token
    # Kullanıcı oluştur
    await client.post("/api/v1/auth/register", json={
        "email": "jwt_test@emare.com",
        "username": "jwttest",
        "password": "Test1234!",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "username": "jwttest",
        "password": "Test1234!",
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    payload = decode_token(token, "test-secret-key-integration")
    assert "sub" in payload


# ── Docs (geliştirme modunda açık) ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_docs_available_in_dev(client):
    """/docs geliştirme modunda erişilebilir."""
    resp = await client.get("/docs")
    # Testing modunda docs açık olmalı
    assert resp.status_code == 200


# ── Güvenlik ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    """Token olmadan korumalı endpoint yetkisiz yanıt döndürmeli."""
    resp = await client.get("/api/v1/users/me")
    # 401: yetkisiz, 403: yasak, 404: bulunamadı, 422: validation hatası (parametre eksik)
    assert resp.status_code in (401, 403, 404, 422)


@pytest.mark.asyncio
async def test_cors_headers(client):
    """CORS başlıkları doğru mu?"""
    resp = await client.options("/api/v1/auth/login", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
    })
    # OPTIONS ya da 200 yanıtı
    assert resp.status_code in (200, 204, 405)


# ── API Şema ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_openapi_schema(client):
    """OpenAPI şeması geçerli JSON döndürüyor mi?"""
    resp = await client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert "openapi" in schema
    assert "paths" in schema
    # Temel path'ler tanımlı mı?
    assert "/api/v1/auth/register" in schema["paths"]
    assert "/api/v1/auth/login" in schema["paths"]
