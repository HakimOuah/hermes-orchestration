from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import EventEnvelope, Signal


def entity_key(event: EventEnvelope) -> str:
    external = event.entity.external_id or event.entity.name or "unknown"
    return f"{event.entity.type}:{external}".lower()


def score_events(events: Iterable[EventEnvelope]) -> list[Signal]:
    """Very small deterministic v0 signal engine.

    The first version deliberately avoids LLM judgement. It rewards:
    - multiple independent sources
    - high-confidence observations
    - explicit growth/velocity metrics

    Later versions can add learned weights and category-specific rules while
    keeping the same event contract.
    """
    grouped: dict[str, list[EventEnvelope]] = defaultdict(list)
    for event in events:
        grouped[entity_key(event)].append(event)

    signals: list[Signal] = []
    for key, group in grouped.items():
        sources = {e.source for e in group}
        avg_conf = sum(e.confidence for e in group) / len(group)

        growth_points = 0.0
        reasons: list[str] = []
        for event in group:
            for metric_name, value in event.metrics.items():
                if not isinstance(value, (int, float)):
                    continue
                name = metric_name.lower()
                if any(token in name for token in ("growth", "velocity", "delta", "increase")):
                    contribution = max(-20.0, min(float(value), 100.0)) * 0.18
                    growth_points += max(0.0, contribution)
                    if value > 0:
                        reasons.append(f"{event.source}:{metric_name}={value}")

        source_points = min(len(sources) * 15.0, 45.0)
        confidence_points = avg_conf * 25.0
        score = max(0.0, min(100.0, source_points + confidence_points + growth_points))

        if score >= 85:
            priority = "critical"
        elif score >= 70:
            priority = "high"
        elif score >= 50:
            priority = "medium"
        else:
            priority = "low"

        reasons.insert(0, f"{len(sources)} independent source(s)")
        signals.append(
            Signal(
                entity_key=key,
                signal_type="market.opportunity",
                source_events=[e.event_id for e in group],
                score=round(score, 2),
                confidence=round(avg_conf, 3),
                priority=priority,
                reasons=reasons[:12],
                metadata={"sources": sorted(sources), "event_count": len(group)},
            )
        )

    return sorted(signals, key=lambda s: s.score, reverse=True)
