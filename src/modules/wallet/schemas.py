"""Wallet Schemas — dijital cüzdan Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Bakiye
# ---------------------------------------------------------------------------

class BalanceSchema(BaseModel):
    """Kullanıcı cüzdan bakiyesi."""

    user_id: str
    balance: Decimal
    currency: str = "TRY"
    updated_at: datetime | None = None


# ---------------------------------------------------------------------------
# Para Yükleme / Çekme İsteği
# ---------------------------------------------------------------------------

class DepositRequest(BaseModel):
    """Para yükleme isteği."""

    amount: Decimal = Field(..., gt=0, description="Yüklenecek tutar")
    description: str | None = None


class WithdrawRequest(BaseModel):
    """Para çekme isteği."""

    amount: Decimal = Field(..., gt=0, description="Çekilecek tutar")
    description: str | None = None


# ---------------------------------------------------------------------------
# Transfer İsteği
# ---------------------------------------------------------------------------

class TransferRequest(BaseModel):
    """Kullanıcılar arası transfer isteği."""

    receiver_id: str
    amount: Decimal = Field(..., gt=0, description="Transfer tutarı")
    description: str | None = None


# ---------------------------------------------------------------------------
# İşlem Yanıtı
# ---------------------------------------------------------------------------

class TransactionSchema(BaseModel):
    """Cüzdan işlem yanıtı."""

    transaction_id: str
    user_id: str | None = None
    sender_id: str | None = None
    receiver_id: str | None = None
    type: str
    amount: Decimal
    description: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
