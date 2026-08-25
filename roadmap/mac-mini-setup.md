# Mac mini Setup Roadmap

## Phase 0 — Before hardware arrives
- keep working with the current Cursor/Grok setup;
- preserve existing product-research documentation and inputs;
- avoid locking the architecture to today's model leaderboard;
- collect representative past tasks for HakimBench.

## Phase 1 — Base machine
- update macOS;
- install package manager and development basics;
- configure automatic login/startup behavior only if appropriate;
- configure backups;
- optionally configure Tailscale;
- decide whether the Mac mini will replace any VPS workloads.

## Phase 2 — Local inference
- install MLX runtime/tooling;
- test the strongest current models that fit comfortably in 48 GB;
- benchmark speed, RAM, long-context behavior and output quality;
- test Ollama/llama.cpp only where useful for compatibility/convenience.

## Phase 3 — Hermes
- install/update Hermes Desktop/runtime;
- expose the chosen local inference endpoint;
- configure model providers/APIs;
- create core agent profiles;
- validate memory and skills behavior;
- validate browser/tool calling.

## Phase 4 — HakimBench
- run blind-ish benchmark on real business tasks;
- compare local vs low-cost APIs vs frontier models;
- record cost and latency;
- produce the first production routing map.

## Phase 5 — Product research pilot
- encode existing product criteria into the product-research playbook;
- integrate available research sources/APIs;
- run one research cycle in shadow mode against the existing workflow;
- compare shortlist quality;
- require human approval for all launches.

## Phase 6 — Learning loop
- create structured experiment records;
- collect launch metrics;
- run post-mortems;
- introduce learned-rules governance;
- recalibrate scoring only with evidence.

## Phase 7 — Cost optimization
- measure actual monthly API consumption;
- identify redundant subscriptions;
- cancel only after replacement workflows have proven reliable;
- reassess whether a VPS is still needed.

## Definition of success
The system succeeds if it produces better product decisions and higher-quality storefront execution with lower recurring model cost — not merely if it runs locally.