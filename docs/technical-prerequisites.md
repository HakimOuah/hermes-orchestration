# Technical Prerequisites — OH Ventures Agent Runtime

This document turns the architecture repo into a deployable foundation for the future Mac mini node.

## Principle

Do not fork or duplicate Hermes internals. Hermes remains the orchestration layer. This repository owns the **OH Ventures control plane** around it:

- normalized events
- watchers/connectors
- signal scoring
- persistent operational memory
- escalation policy
- audit logs
- agent permissions
- business-specific playbooks

## Mac mini baseline

Target: Apple Silicon macOS, 64 GB unified memory.

Install/verify:

- Xcode command-line tools
- Homebrew
- Git
- Hermes Agent
- Ollama or another OpenAI-compatible local inference server
- Docker Desktop (optional initially, useful when Redis/Postgres/services are introduced)
- Python tooling via `uv`

Hermes' official installer already manages most of its own dependencies; our scripts should therefore stay idempotent and avoid conflicting Python/Node installations.

## Runtime phases

### Phase 0 — laptop-safe development

Before the Mac mini arrives we can already develop and test with:

- Python 3.11+
- SQLite
- mocked external APIs
- optional local LLM
- dry-run / shadow mode only

### Phase 1 — Mac mini bootstrap

- install Hermes
- install local inference runtime
- clone this repository
- copy `.env.example` to `.env`
- run prerequisite check
- initialize runtime database
- start one watcher and Signal Engine

### Phase 2 — first production loop

Start with the smallest valuable loop:

```text
TrendTrack watcher
      -> raw event
      -> normalized signal
      -> Signal Engine
      -> candidate score
      -> shadow investigation
      -> Morning Brief
```

No autonomous external writes.

### Phase 3 — multi-source confirmation

Add independent sources and only escalate when multiple signals agree.

### Phase 4 — Hermes dispatch

Hermes receives high-priority events and assigns specialist agents according to the Agent Constitution.

## Initial local services

Keep version 1 intentionally boring.

### SQLite

Use SQLite first for:
- event journal
- signals
- investigations
- decisions
- outcomes
- agent actions

This makes local development and backups trivial.

Move to Postgres only once concurrency or analytics justify it.

### Filesystem artifact store

Keep large HTML/JSON/screenshot artifacts outside the database and store references plus hashes in the event journal.

### Optional Redis

Do not require Redis on day one. Introduce it when concurrent workers need a queue or pub/sub bus.

## Event-driven architecture

Every watcher emits a common event envelope.

```json
{
  "event_id": "uuid",
  "event_type": "market.shop_growth",
  "source": "trendtrack",
  "observed_at": "ISO-8601",
  "entity": {
    "type": "shop",
    "external_id": "...",
    "name": "..."
  },
  "metrics": {},
  "raw_ref": null,
  "confidence": 0.8,
  "metadata": {}
}
```

The Signal Engine must consume normalized events rather than provider-specific payloads.

## Secrets

Never commit API keys.

Secrets live in `.env` locally at first and later may move to macOS Keychain or another secret manager.

Minimum planned secrets:

- TrendTrack API key
- frontier model API keys
- optional Shopify / Meta / Google credentials
- optional notification endpoints

## Logging

Every meaningful agent action should include:

- actor / agent
- input event(s)
- model/provider
- prompt/playbook version
- action proposed
- autonomy level
- confidence
- estimated impact
- result
- human override if any

The objective is replayability and post-mortem analysis.

## Shadow mode first

The first production deployment should not mutate Shopify, ads, code, budgets, emails or external systems.

It observes and records what it *would* have done.

This produces calibration data before autonomy is granted.

## Next technical milestones

1. Mac bootstrap and health-check scripts.
2. Runtime Python package.
3. Event schema and SQLite journal.
4. TrendTrack connector client.
5. Generic watcher scheduler.
6. Signal Engine v0.
7. Shadow investigation runner.
8. Morning Brief generator.
9. Hermes adapter.
10. Multi-source connectors.
