# Hermes Orchestration

A practical blueprint for running an AI-first e-commerce operating system with Hermes as the orchestrator, local open-weight models for high-volume work, and frontier models for high-value reasoning and audits.

## Core philosophy

The system is deliberately asymmetric:

- **Frontier models = senior strategy / policy / audit.** They convert business intent into strict execution specs, challenge assumptions, audit critical outputs, and make or review high-value decisions.
- **Local models = execution at scale.** They handle the bulk of research, extraction, classification, scoring, synthesis, iteration, competitor analysis, review mining, SEO drafts, copy drafts, translations, and repetitive analysis.
- **Hermes = orchestration layer.** It routes work, invokes tools, persists memory, applies skills, coordinates agents, and manages the feedback loop.
- **GitHub = source of truth.** Playbooks, scoring rules, learned rules, benchmark tasks, and post-mortems are versioned rather than silently drifting.
- **Business outcomes = learning signal.** The system should improve from launches and failures, not merely from model confidence.

## Target architecture

```text
User
  |
  v
Frontier policy / strategist
  |
  v
Hermes Orchestrator
  |
  +--> Local LLMs on Mac mini
  |      - product research
  |      - competitor analysis
  |      - review mining
  |      - SEO / GMC pre-checks
  |      - copy drafts
  |      - data cleanup / scoring
  |
  +--> Low-cost API models
  |      - second opinions
  |      - deeper market analysis
  |
  +--> Frontier APIs
         - final audit
         - adversarial critique
         - critical decisions
```

## Product-learning loop

```text
Research -> Decision -> Launch -> Results -> Post-mortem -> Update playbook
```

Each launch becomes an experiment. The system stores what it predicted, what happened, why the prediction was wrong or right, and which rules should change. The objective is not generic "AI memory" but a progressively better proprietary product-selection system.

## Initial repo map

- `docs/architecture.md` — complete system architecture
- `docs/model-routing.md` — local/API/frontier routing strategy
- `docs/cost-strategy.md` — cost-control principles
- `docs/mac-mini-ai-server.md` — target Mac mini setup
- `docs/product-research-system.md` — end-to-end weekly research workflow
- `docs/learning-loop.md` — structured self-improvement loop
- `agents/` — proposed agent roles
- `playbooks/` — procedures to be encoded as Hermes skills later
- `scoring/` — product scoring and learned rules
- `benchmarks/hakimbench.md` — future benchmark on real business tasks
- `roadmap/mac-mini-setup.md` — rollout plan when the Mac mini arrives

## Important principle

Do **not** let the system silently rewrite its own product-selection policy. Proposed rule changes should be explicit, evidenced, versioned, and reversible.

This repository is currently a design/specification repository. The implementation phase will start after the local hardware is available and current open-weight models have been re-benchmarked.