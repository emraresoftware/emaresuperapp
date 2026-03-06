"""
Emare SuperApp — Birim Testleri
"""
import pytest


def test_app_name():
    """Uygulama adı doğru mu?"""
    from src.utils.constants import APP_NAME
    assert APP_NAME == "Emare SuperApp"


def test_password_hash():
    """Şifre hashleme çalışıyor mu?"""
    from src.core.security import hash_password, verify_password
    hashed = hash_password("test123")
    assert verify_password("test123", hashed)
    assert not verify_password("wrong", hashed)


def test_token_create_and_decode():
    """JWT token oluştur ve çöz."""
    from src.core.security import create_access_token, decode_token
    secret = "test-secret"
    token = create_access_token({"sub": "emre"}, secret)
    payload = decode_token(token, secret)
    assert payload["sub"] == "emre"


def test_event_bus():
    """Event bus basit test."""
    import asyncio
    from src.core.events import EventBus

    bus = EventBus()
    results = []

    async def handler(data):
        results.append(data)

    bus.on("test", handler)

    asyncio.get_event_loop().run_until_complete(bus.emit("test", "hello"))
    assert results == ["hello"]
