"""Wallet Service — dijital cüzdan işlemleri."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import uuid4


# ---------------------------------------------------------------------------
# Bakiye Sorgulama
# ---------------------------------------------------------------------------

async def get_balance(user_id: str) -> dict[str, Any]:
    """Kullanıcının güncel cüzdan bakiyesini döndürür.

    Returns:
        Bakiye bilgilerini içeren sözlük.
    """
    # TODO: Veritabanından bakiye bilgisi çek
    return {
        "user_id": user_id,
        "balance": "0.00",
        "currency": "TRY",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Para Yükleme
# ---------------------------------------------------------------------------

async def deposit(
    user_id: str,
    amount: Decimal,
    description: str | None = None,
) -> dict[str, Any]:
    """Cüzdana para yükler.

    Args:
        user_id: Hedef kullanıcı kimliği.
        amount: Yüklenecek tutar (pozitif olmalı).
        description: İşlem açıklaması.

    Returns:
        İşlem detaylarını içeren sözlük.
    """
    if amount <= 0:
        raise ValueError("Yükleme tutarı pozitif olmalıdır.")

    tx_id = str(uuid4())

    # TODO: Veritabanında bakiyeyi güncelle ve işlem kaydı oluştur
    return {
        "transaction_id": tx_id,
        "user_id": user_id,
        "type": "deposit",
        "amount": str(amount),
        "description": description,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Para Çekme
# ---------------------------------------------------------------------------

async def withdraw(
    user_id: str,
    amount: Decimal,
    description: str | None = None,
) -> dict[str, Any]:
    """Cüzdandan para çeker.

    Args:
        user_id: Kaynak kullanıcı kimliği.
        amount: Çekilecek tutar (pozitif olmalı).
        description: İşlem açıklaması.

    Returns:
        İşlem detaylarını içeren sözlük.

    Raises:
        ValueError: Yetersiz bakiye veya geçersiz tutar.
    """
    if amount <= 0:
        raise ValueError("Çekim tutarı pozitif olmalıdır.")

    # TODO: Bakiye kontrolü yap
    # TODO: Veritabanında bakiyeyi güncelle ve işlem kaydı oluştur

    tx_id = str(uuid4())
    return {
        "transaction_id": tx_id,
        "user_id": user_id,
        "type": "withdraw",
        "amount": str(amount),
        "description": description,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Transfer
# ---------------------------------------------------------------------------

async def transfer(
    sender_id: str,
    receiver_id: str,
    amount: Decimal,
    description: str | None = None,
) -> dict[str, Any]:
    """Kullanıcılar arası bakiye transferi yapar.

    Args:
        sender_id: Gönderen kullanıcı kimliği.
        receiver_id: Alıcı kullanıcı kimliği.
        amount: Transfer tutarı (pozitif olmalı).
        description: İşlem açıklaması.

    Returns:
        Transfer detaylarını içeren sözlük.

    Raises:
        ValueError: Yetersiz bakiye, geçersiz tutar veya kendi kendine transfer.
    """
    if amount <= 0:
        raise ValueError("Transfer tutarı pozitif olmalıdır.")
    if sender_id == receiver_id:
        raise ValueError("Kendi cüzdanınıza transfer yapamazsınız.")

    # TODO: Gönderenin bakiyesini kontrol et
    # TODO: Atomik işlem ile her iki bakiyeyi güncelle

    tx_id = str(uuid4())
    return {
        "transaction_id": tx_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "type": "transfer",
        "amount": str(amount),
        "description": description,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
