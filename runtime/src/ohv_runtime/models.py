from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class EntityRef(BaseModel):
    type: str
    external_id: str | None = None
    name: str | None = None
    url: str | None = None


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    source: str
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    entity: EntityRef
    metrics: dict[str, float | int | str | bool | None] = Field(default_factory=dict)
    raw_ref: str | None = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Signal(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid4()))
    entity_key: str
    signal_type: str
    source_events: list[str]
    score: float = Field(ge=0.0, le=100.0)
    confidence: float = Field(ge=0.0, le=1.0)
    priority: Literal["low", "medium", "high", "critical"]
    reasons: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
