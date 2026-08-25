# Architecture

## Goal

Build an AI operating system for e-commerce where the majority of token-heavy work is performed locally, while expensive frontier models are reserved for strict specification, adversarial review, and high-value decisions.

## Roles

### User
Defines business intent, constraints, budget, appetite for risk, and final launch decisions.

### Frontier strategist / policy layer
Used selectively for tasks such as:
- converting a natural-language request into a strict machine-executable research brief;
- challenging product theses;
- auditing copywriting and positioning;
- final review of high-risk GMC/compliance issues;
- deciding where uncertainty is too high for automatic execution.

### Hermes orchestrator
Responsible for:
- decomposing missions;
- assigning agents;
- selecting tools and models;
- enforcing budgets and policies;
- persisting useful memory;
- coordinating review loops;
- recording experiments and outcomes.

### Local execution layer
Runs primarily on the Mac mini. It should absorb high-volume work including research, extraction, deduplication, clustering, scoring, review mining, competitor synthesis, draft copy, SEO work, and repeated iterations.

### Low-cost API layer
Used when a stronger or independent second opinion is needed but a full frontier model is not justified.

### Frontier API layer
Used for scarce, high-value reasoning and final audits.

## Hardware concept

Primary target:
- Mac mini M4 Pro
- 48 GB unified memory
- local inference through MLX where practical
- Hermes backend and agents running continuously
- remote access optional through Tailscale

Secondary machine:
- MacBook Air M3 24 GB as optional cockpit / fallback / lightweight local inference machine

The preferred workflow, however, is to work directly on the Mac mini when convenient.

## Design principles

1. **Cheap first, expensive last.** Do not invoke frontier models before local models have reduced the problem to the smallest useful context.
2. **Evidence before opinion.** Product recommendations must cite or store the underlying market evidence.
3. **Adversarial review.** Final reviewers should actively search for reasons a thesis is wrong.
4. **Versioned learning.** Scoring changes and learned rules are explicit Git changes, never silent drift.
5. **Outcome-driven improvement.** Real launch metrics are more valuable than model confidence.
6. **Human control for consequential decisions.** Product launch, significant spend, supplier commitment, and policy-sensitive publication remain approval gates.

## Long-term vision

After enough research cycles and launches, the repository should contain a proprietary dataset linking:
- initial research signals;
- predicted scores;
- final launch choices;
- ad and site metrics;
- margins, refunds and operational issues;
- post-mortem conclusions;
- resulting rule changes.

That dataset can later support statistical calibration, retrieval, specialized classifiers, or fine-tuning if the volume becomes sufficient.