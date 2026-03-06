"""
Emare SuperApp — Users API Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


@router.get("/", response_model=List[UserResponse])
async def list_users():
    """Tüm kullanıcıları listele."""
    # TODO: DB'den çek
    return []


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Tek kullanıcı detayı."""
    return UserResponse(id=user_id, email="demo@emare.com", username="emre")


@router.put("/{user_id}")
async def update_user(user_id: int):
    """Kullanıcı güncelle."""
    return {"message": f"Kullanıcı {user_id} güncellendi"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Kullanıcı sil."""
    return {"message": f"Kullanıcı {user_id} silindi"}
