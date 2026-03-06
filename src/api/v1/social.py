"""
Emare SuperApp — Social API Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class PostResponse(BaseModel):
    id: int
    author: str
    content: str
    likes: int = 0
    created_at: Optional[str] = None


class CreatePostRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    sender: str
    receiver: str
    content: str
    is_read: bool = False


@router.get("/feed", response_model=List[PostResponse])
async def get_feed():
    """Sosyal akış."""
    return []


@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(data: CreatePostRequest):
    """Gönderi paylaş."""
    return PostResponse(id=1, author="emre", content=data.content)


@router.post("/posts/{post_id}/like")
async def like_post(post_id: int):
    """Gönderiyi beğen."""
    return {"message": f"Gönderi {post_id} beğenildi"}


@router.get("/messages", response_model=List[MessageResponse])
async def list_messages():
    """Mesajlar."""
    return []


@router.post("/messages")
async def send_message(receiver: str, content: str):
    """Mesaj gönder."""
    return {"message": f"Mesaj {receiver}'ye gönderildi"}
