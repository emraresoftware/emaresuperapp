"""
Emare SuperApp — Marketplace API Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    currency: str = "TRY"
    category: Optional[str] = None
    is_active: bool = True


class CreateProductRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: Optional[int] = None


@router.get("/products", response_model=List[ProductResponse])
async def list_products():
    """Ürünleri listele."""
    return []


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Ürün detayı."""
    return ProductResponse(id=product_id, name="Demo Ürün", price=99.90)


@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(data: CreateProductRequest):
    """Yeni ürün ekle."""
    return ProductResponse(id=1, name=data.name, price=data.price)


@router.get("/categories")
async def list_categories():
    """Kategorileri listele."""
    return [
        {"id": 1, "name": "SaaS", "slug": "saas"},
        {"id": 2, "name": "Altyapı", "slug": "altyapi"},
        {"id": 3, "name": "AI", "slug": "ai"},
        {"id": 4, "name": "Güvenlik", "slug": "guvenlik"},
    ]


@router.post("/products/{product_id}/purchase")
async def purchase(product_id: int):
    """Ürün satın al."""
    return {"message": f"Ürün {product_id} satın alındı"}
