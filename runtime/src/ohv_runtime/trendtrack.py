from __future__ import annotations

from typing import Any

import httpx

from .config import Settings


class TrendTrackClient:
    """Thin client around TrendTrack's public API.

    Endpoint selection should follow TrendTrack's agent guide rather than be
    hard-coded into business logic. Watchers call this generic request method
    and normalize provider payloads into OHV EventEnvelope objects.

    Agent guide:
    https://docs.trendtrack.io/docs/agent-guide.md
    """

    def __init__(self, settings: Settings):
        if not settings.trendtrack_api_key:
            raise ValueError("TRENDTRACK_API_KEY is not configured")
        self.base_url = settings.trendtrack_base_url.rstrip("/")
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=30.0,
            headers={"Authorization": f"Bearer {settings.trendtrack_api_key}"},
        )

    def request(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def verify(self) -> dict[str, Any]:
        """Verify API authentication with TrendTrack's unmetered identity route."""
        return self.request("/v1/me")

    def usage(self) -> dict[str, Any]:
        """Read current API credit usage before metered market queries."""
        return self.request("/v1/usage")

    def freshness(self) -> dict[str, Any]:
        """Check latest-ready data date before freshness-sensitive analytics."""
        return self.request("/v1/system/freshness")

    def lookup(self, query: str) -> dict[str, Any]:
        """Resolve a supplied brand/domain/handle before deeper requests."""
        return self.request("/v1/lookup", params={"q": query})

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "TrendTrackClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
