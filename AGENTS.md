# AGENTS.md — hermes-orchestration

Read by Codex, Cursor and any agent following the `AGENTS.md` convention.
**It duplicates no rule** — it says where the rules are.

Written in English to match this repository; the four other repos of the project are in French.

## Where this repository sits

Part of a five-repository project driven from the hub
[boutiques-drop](https://github.com/HakimOuah/boutiques-drop), cloned locally at
`~/Documents/Boutiques drop/`. **This repo is deliberately cloned outside that tree**
(decision 2026-08-30).

**This repository never holds the business method** (decision 2026-08-30, see
`docs/audit-2026-08-30.md`). The method lives in the hub and in `boutique-pipeline`.
This repo holds orchestration, the mission journal and the benchmark, and *points* to the
method without copying it. Do not import method content here.

Transverse rules — GitHub as source of truth, commit and push at the end of every task,
what is never committed: `~/Documents/Boutiques drop/CLAUDE.md`.

## NOX editorial journal — after every significant step

NOX is Hakim's X account on **AI Agents × Automation × E-commerce**. So that it can talk about
what actually ships, **the agent that completes a significant step writes a structured editorial
event before handing back** — at commit time, not later.

Events are centralised in the hub, never here: NOX reads one directory for all five repos.

**Record:** a new project, a new store, a new agent or role, a new automation, a new integration,
a new API; a method rule learned or invalidated; a first real number (a launch, a cost, a failure
that taught something).

**Do not record:** typos, trivial refactors, cosmetic changes, housekeeping Git operations,
technical changes without consequence. **When in doubt, do not write.**

The mission journal (`missions/<id>/journal.jsonl` — per-call role, model, tokens, cost, verdict)
is machine telemetry and is **never** a NOX event. An event is what a human would tell another
human. A run that produced no new capability and no new knowledge produces no event, however
many calls it logged.

```bash
python3 "$HOME/Documents/Boutiques drop/scripts/nox-evenement.py" \
  --categorie <agent|automatisation|integration|api|projet|methode|resultat> \
  --titre "..." --projet hermes --repo hermes-orchestration --axes agents,automatisation
```

Then fill in the body of the created file — the section *« Le détail qui fait le contenu »*
first: what surprised you, what broke, the exact number, the false lead followed before it
worked. That section is the only one that cannot be reconstructed from Git later, and the
validator rejects an event that leaves it empty.

Commit the created event **in the hub**, not in this repo.

An agent always writes `statut_editorial: brut` and stops there. Promotion to `retenu` or
`publie` is Hakim's decision alone — the same governance principle this repository already
states: *do not let the system silently rewrite its own business policy*, and the same rule
that forbids promoting a learned rule in `scoring/learned-rules.md` without human agreement.

Full rule, significance test and schema: `~/Documents/Boutiques drop/nox/README.md`.
That is the single source — do not copy it here.
