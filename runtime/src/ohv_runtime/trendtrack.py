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

    def lookup(self, query: str) -> dict[str, Any]:
        """Resolve a supplied brand/domain/handle before deeper requests.

        TrendTrack's agent documentation recommends lookup first when a user
        provides an identifiable brand/domain/handle/page id.
        """
        return self.request("/v1/lookup", params={"query": query})

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "TrendTrackClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
