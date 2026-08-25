# Cost Strategy

## Principle

Treat intelligence as a routed resource rather than a bundle of overlapping subscriptions.

Target end state:
- local inference for most token volume;
- usage-based APIs for specialist models;
- at most one premium consumer subscription retained as a convenient backup/interface if it still provides enough value.

## Monthly budget controls

Hermes should eventually track model spend per mission and per product research cycle.

Example policy:

```yaml
monthly_ai_budget_eur: 50
local_inference: unlimited
low_cost_api_budget_eur: 20
frontier_api_budget_eur: 30
require_reason_if_single_task_cost_eur_gt: 1
require_human_approval_if_single_task_cost_eur_gt: 3
```

Numbers are placeholders and should be calibrated from real API usage.

## Cost accounting per mission

Each mission should record:
- model used;
- input/output tokens when available;
- estimated cost;
- purpose of escalation;
- result quality;
- whether escalation materially improved the decision.

Example:

```text
PR-042
Local Qwen       1.8M tokens    ~electricity only
Low-cost API     180k tokens    €x.xx
Frontier audit    40k tokens    €x.xx
Total                            €x.xx
```

## Subscription strategy

Do not cancel useful subscriptions based only on theoretical savings. Benchmark the replacement workflow first, then remove subscriptions once the local/API setup has demonstrated equivalent or better utility.

The three-month discounted Cursor/Grok period can be used as a comparison window against the future local stack.