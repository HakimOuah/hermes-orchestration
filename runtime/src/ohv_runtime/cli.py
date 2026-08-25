from __future__ import annotations

import json
from pathlib import Path

import httpx
import typer

from .config import Settings
from .journal import Journal
from .models import EntityRef, EventEnvelope
from .signal_engine import score_events

app = typer.Typer(no_args_is_help=True)


@app.command()
def init() -> None:
    """Initialize local runtime directories and SQLite schema."""
    settings = Settings()
    settings.ensure_dirs()
    Journal(settings.ohv_db_path)
    typer.echo(f"Initialized OHV runtime at {settings.ohv_db_path}")
    typer.echo(f"Shadow mode: {settings.ohv_shadow_mode}")


@app.command()
def health() -> None:
    """Check filesystem, database and optional local inference availability."""
    settings = Settings()
    settings.ensure_dirs()
    Journal(settings.ohv_db_path)

    status = {
        "database": "ok",
        "artifact_dir": "ok" if settings.ohv_artifact_dir.exists() else "missing",
        "shadow_mode": settings.ohv_shadow_mode,
        "trendtrack_key": "configured" if settings.trendtrack_api_key else "missing",
        "local_llm": "unknown",
    }

    try:
        response = httpx.get(settings.local_llm_base_url, timeout=2.0)
        status["local_llm"] = f"reachable:{response.status_code}"
    except Exception:
        status["local_llm"] = "unreachable"

    typer.echo(json.dumps(status, indent=2))


@app.command("demo-signal")
def demo_signal() -> None:
    """Run the deterministic signal engine against synthetic multi-source events."""
    events = [
        EventEnvelope(
            event_type="market.shop_growth",
            source="trendtrack",
            entity=EntityRef(type="product", external_id="demo-product", name="Demo Product"),
            metrics={"growth30d": 72, "ads_increase": 45},
            confidence=0.85,
        ),
        EventEnvelope(
            event_type="market.search_growth",
            source="google_trends",
            entity=EntityRef(type="product", external_id="demo-product", name="Demo Product"),
            metrics={"search_growth": 38},
            confidence=0.75,
        ),
    ]
    signals = score_events(events)
    typer.echo(json.dumps([s.model_dump(mode="json") for s in signals], indent=2))


if __name__ == "__main__":
    app()
