# Hermes Orchestration

A practical blueprint for building an **agent-native OH Ventures operating system** with Hermes as orchestrator, local open-weight models for high-volume cognition, and frontier models for high-value reasoning, adversarial review and audits.

## Core philosophy

The system is deliberately asymmetric:

- **Frontier models = senior strategy / policy / audit.** They convert business intent into strict execution specs, challenge assumptions, audit critical outputs, and make or review high-value decisions.
- **Local models = execution at scale.** They handle the bulk of observation, research, extraction, classification, scoring, synthesis, iteration, competitor analysis, review mining, SEO drafts, copy drafts, translations, and repetitive analysis.
- **Hermes = orchestration layer.** It routes work, invokes tools, persists memory, applies skills, coordinates agents, manages events and runs feedback loops.
- **GitHub = source of truth.** Playbooks, scoring rules, learned rules, benchmark tasks, policies and post-mortems are versioned rather than silently drifting.
- **Business outcomes = learning signal.** The system should improve from launches and failures, not merely from model confidence.
- **Human = strategy, judgment and capital allocation.** Automation should increase leverage while preserving human authority over consequential decisions.

## Target architecture

```text
Human
  |
  v
Hermes Orchestrator
  |
  +--> Watchers / Researchers / Workers / Builders
  |      |
  |      +--> Local LLMs on Mac mini
  |      +--> deterministic tools / APIs
  |
  +--> confidence / impact / disagreement gates
  |      |
  |      +--> Low-cost API models
  |      +--> Frontier models
  |             - strategy
  |             - adversarial critique
  |             - audit
  |             - difficult arbitration
  |
  +--> Human approval for material decisions
```

## Operating loop

```text
Observe -> Detect -> Hypothesize -> Challenge -> Decide -> Act -> Measure -> Learn
```

The system should be event-driven. Cheap watchers observe continuously; expensive reasoning activates only when an event deserves it.

## Product-learning loop

```text
Research -> Prediction -> Decision -> Launch -> Results -> Post-mortem -> Update knowledge
```

Each launch becomes an experiment. The system stores what it predicted, what happened, why the prediction was wrong or right, and which rules should change. The objective is not generic "AI memory" but progressively better proprietary decision systems.

## Repository map

### Core architecture
- `docs/architecture.md` — complete system architecture
- `docs/always-on-agent-operating-system.md` — H24 agent portfolio and OH Ventures OS vision
- `docs/agent-constitution.md` — autonomy levels, Shadow Mode, escalation, Skeptic, governance and human control
- `docs/model-routing.md` — local/API/frontier routing strategy
- `docs/cost-strategy.md` — cost-control principles
- `docs/mac-mini-ai-server.md` — target Mac mini setup

### Market & e-commerce intelligence
- `docs/market-intelligence-engine.md` — TrendTrack-centered signal engine, Business Genome and cross-source opportunity detection
- `docs/product-research-system.md` — end-to-end research workflow
- `docs/learning-loop.md` — structured self-improvement loop

### Operational assets
- `agents/` — proposed agent roles
- `playbooks/` — procedures to be encoded as Hermes skills later
- `scoring/` — product scoring and learned rules
- `benchmarks/hakimbench.md` — benchmark on real business tasks
- `roadmap/mac-mini-setup.md` — rollout plan when local hardware arrives

## Autonomy principle

Agents should progress through bounded autonomy rather than receiving unrestricted permissions.

```text
L0 Observe
L1 Recommend
L2 Prepare
L3 Execute reversible actions
L4 Execute within budget/policy
L5 Narrow policy-bounded autonomy
```

New decision agents should operate in Shadow Mode before promotion.

## Important principle

Do **not** let the system silently rewrite its own business policy. Proposed rule changes should be explicit, evidenced, versioned, auditable and reversible.

## Long-term moat

The strategic asset is the accumulated prediction-to-outcome dataset:

```text
What we observed
      +
What we predicted
      +
What we decided
      +
What we executed
      +
What actually happened
      =
Proprietary operational intelligence
```

The long-term objective is an OH Ventures intelligence layer shared across brands and projects, where validated learning compounds rather than remaining trapped inside individual workflows.

This repository is currently a design/specification repository. Implementation should be staged, benchmarked and progressively granted autonomy.