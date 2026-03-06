"""
Emare SuperApp — Product & Category Modelleri (Marketplace)
"""
from sqlalchemy import String, Numeric, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import BaseModel


class Category(BaseModel):
    """Ürün kategorisi."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

    products: Mapped[List["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(BaseModel):
    """Marketplace ürünü / servisi."""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    currency: Mapped[str] = mapped_column(String(3), default="TRY")
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

    category: Mapped[Optional[Category]] = relationship(back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} | {self.price} {self.currency}>"
