"""Social Schemas — sosyal modül Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Gönderi
# ---------------------------------------------------------------------------

class PostCreateRequest(BaseModel):
    """Yeni gönderi oluşturma isteği."""

    content: str = Field(..., max_length=5000)
    media_urls: list[str] = Field(default_factory=list)


class PostSchema(BaseModel):
    """Gönderi detay yanıtı."""

    id: str
    user_id: str
    content: str
    media_urls: list[str] = Field(default_factory=list)
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Yorum
# ---------------------------------------------------------------------------

class CommentCreateRequest(BaseModel):
    """Yorum oluşturma isteği."""

    content: str = Field(..., max_length=2000)


class CommentSchema(BaseModel):
    """Yorum detay yanıtı."""

    id: str
    user_id: str
    post_id: str
    content: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Takip
# ---------------------------------------------------------------------------

class FollowSchema(BaseModel):
    """Takip bilgisi."""

    follower_id: str
    target_id: str
    created_at: datetime | None = None


# ---------------------------------------------------------------------------
# Profil
# ---------------------------------------------------------------------------

class ProfileSchema(BaseModel):
    """Kullanıcı sosyal profil yanıtı."""

    user_id: str
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Akış
# ---------------------------------------------------------------------------

class FeedResponse(BaseModel):
    """Sayfalı sosyal akış yanıtı."""

    items: list[PostSchema] = Field(default_factory=list)
    page: int = 1
    page_size: int = 20
    total: int = 0
