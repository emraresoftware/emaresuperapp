"""Analytics Schemas — analitik Pydantic şemaları."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Olay Kaydı
# ---------------------------------------------------------------------------

class TrackEventRequest(BaseModel):
    """Olay kaydetme isteği."""

    event_name: str = Field(..., max_length=100)
    properties: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None


class EventSchema(BaseModel):
    """Kaydedilmiş olay yanıtı."""

    event_id: str
    user_id: str | None = None
    event_name: str
    properties: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None
    timestamp: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Özet
# ---------------------------------------------------------------------------

class PeriodFilter(BaseModel):
    """Tarih aralığı filtresi."""

    start_date: str | None = None
    end_date: str | None = None


class SummarySchema(BaseModel):
    """Platform özet istatistikleri."""

    total_users: int = 0
    active_sessions: int = 0
    total_events: int = 0
    total_transactions: int = 0
    period: PeriodFilter = Field(default_factory=PeriodFilter)


# ---------------------------------------------------------------------------
# Kullanıcı Analitik
# ---------------------------------------------------------------------------

class UserAnalyticsSchema(BaseModel):
    """Kullanıcı bazlı analitik yanıtı."""

    user_id: str
    session_count: int = 0
    event_count: int = 0
    most_used_features: list[str] = Field(default_factory=list)
    period: PeriodFilter = Field(default_factory=PeriodFilter)


# ---------------------------------------------------------------------------
# Popüler Olaylar
# ---------------------------------------------------------------------------

class TopEventSchema(BaseModel):
    """Popüler olay bilgisi."""

    event_name: str
    count: int


# ---------------------------------------------------------------------------
# Gerçek Zamanlı
# ---------------------------------------------------------------------------

class PlatformDistribution(BaseModel):
    """Platform dağılımı."""

    web: int = 0
    ios: int = 0
    android: int = 0


class RealtimeSchema(BaseModel):
    """Gerçek zamanlı aktif kullanıcı bilgisi."""

    active_users: int = 0
    by_platform: PlatformDistribution = Field(default_factory=PlatformDistribution)
    timestamp: datetime | None = None
