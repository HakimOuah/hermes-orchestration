from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import EventEnvelope, Signal


SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    source TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_external_id TEXT,
    entity_name TEXT,
    payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_type_time
ON events(event_type, observed_at);

CREATE INDEX IF NOT EXISTS idx_events_source_time
ON events(source, observed_at);

CREATE TABLE IF NOT EXISTS signals (
    signal_id TEXT PRIMARY KEY,
    entity_key TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    score REAL NOT NULL,
    confidence REAL NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL,
    payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_signals_priority_time
ON signals(priority, created_at);
"""


class Journal:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def append_event(self, event: EventEnvelope) -> None:
        self.conn.execute(
            """
            INSERT OR IGNORE INTO events
            (event_id, event_type, source, observed_at, entity_type,
             entity_external_id, entity_name, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.event_type,
                event.source,
                event.observed_at.isoformat(),
                event.entity.type,
                event.entity.external_id,
                event.entity.name,
                event.model_dump_json(),
            ),
        )
        self.conn.commit()

    def append_signal(self, signal: Signal) -> None:
        self.conn.execute(
            """
            INSERT OR IGNORE INTO signals
            (signal_id, entity_key, signal_type, score, confidence,
             priority, created_at, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal.signal_id,
                signal.entity_key,
                signal.signal_type,
                signal.score,
                signal.confidence,
                signal.priority,
                signal.created_at.isoformat(),
                signal.model_dump_json(),
            ),
        )
        self.conn.commit()

    def recent_events(self, limit: int = 100) -> list[dict]:
        rows = self.conn.execute(
            "SELECT payload_json FROM events ORDER BY observed_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [json.loads(row[0]) for row in rows]
