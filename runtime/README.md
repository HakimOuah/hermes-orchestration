# OH Ventures Runtime

Executable foundation for the OH Ventures agent operating system.

## What exists now

- environment configuration
- normalized event model
- normalized signal model
- SQLite event/signal journal
- deterministic Signal Engine v0
- TrendTrack API client skeleton
- CLI healthcheck
- synthetic multi-source signal demo

## Local quickstart

```bash
cd runtime
cp .env.example .env
uv sync
uv run ohv init
uv run ohv health
uv run ohv demo-signal
```

## Why deterministic first?

The first Signal Engine deliberately avoids using an LLM to decide whether a market event is important. This gives us a transparent baseline that can be replayed and measured.

Later layers can add:

1. learned weights
2. category-specific rules
3. local-model enrichment
4. frontier-model escalation

without changing the event contract.

## Data flow

```text
Provider payload
   -> connector
   -> EventEnvelope
   -> Journal
   -> Signal Engine
   -> Signal
   -> Shadow investigation
   -> Hermes
   -> specialist agents
```

## Safety default

`OHV_SHADOW_MODE=true` is the default. The runtime should not perform business mutations until explicit autonomy is granted under the Agent Constitution.

## TrendTrack

TrendTrack endpoint choice should follow its current agent-oriented API documentation. The client intentionally provides a small generic request layer instead of embedding lots of potentially stale endpoint assumptions into business logic.

## Planned next files

- `watchers/trendtrack_scaling.py`
- `investigations/market.py`
- `briefing/morning.py`
- `routing/escalation.py`
- `hermes/adapter.py`
- connectors for independent confirmation sources
