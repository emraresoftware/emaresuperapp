"""Marketplace Schemas — pazaryeri Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Ürün
# ---------------------------------------------------------------------------

class ProductCreateRequest(BaseModel):
    """Yeni ürün oluşturma isteği."""

    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=5000)
    price: Decimal = Field(..., gt=0)
    category: str | None = None
    images: list[str] = Field(default_factory=list)


class ProductUpdateRequest(BaseModel):
    """Ürün güncelleme isteği — yalnızca gönderilen alanlar güncellenir."""

    title: str | None = Field(None, max_length=200)
    description: str | None = Field(None, max_length=5000)
    price: Decimal | None = Field(None, gt=0)
    category: str | None = None
    images: list[str] | None = None


class ProductSchema(BaseModel):
    """Ürün detay yanıtı."""

    id: str
    seller_id: str
    title: str
    description: str
    price: Decimal
    category: str | None = None
    images: list[str] = Field(default_factory=list)
    status: str = "active"
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Sipariş
# ---------------------------------------------------------------------------

class OrderCreateRequest(BaseModel):
    """Sipariş oluşturma isteği."""

    product_id: str
    quantity: int = Field(1, ge=1)


class OrderSchema(BaseModel):
    """Sipariş detay yanıtı."""

    order_id: str
    buyer_id: str
    product_id: str
    quantity: int
    status: str = "pending"
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Liste Yanıtı
# ---------------------------------------------------------------------------

class ProductListResponse(BaseModel):
    """Sayfalı ürün listesi yanıtı."""

    items: list[ProductSchema] = Field(default_factory=list)
    page: int = 1
    page_size: int = 20
    total: int = 0
