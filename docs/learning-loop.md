# Learning Loop

## What "self-learning" should mean here

Do not rely on the language model retraining itself after every task. The practical learning loop should combine:
- persistent memory;
- reusable Hermes skills;
- versioned playbooks;
- structured experiment records;
- post-mortems;
- scoring calibration from real business outcomes.

## Core loop

```text
Research
  -> prediction
  -> launch decision
  -> real-world result
  -> post-mortem
  -> proposed rule changes
  -> review
  -> versioned playbook update
```

## Experiment record

Every launched product should eventually contain at least:

```yaml
product_id: PRODUCT-042
research_mission_id: PR-042
predicted_success_score: 82
scores:
  demand: 8.7
  competition: 7.4
  pain: 9.1
  margin: 8.2
  differentiation: 6.8
  creative_potential: 9.0
  gmc_safety: 8.8
actuals:
  ctr: null
  cvr: null
  cpa_eur: null
  aov_eur: null
  refund_rate_pct: null
  net_margin_pct: null
outcome: pending
```

## Post-mortem questions

For every meaningful winner or failure:
1. What did the system predict correctly?
2. What did it predict incorrectly?
3. Which evidence was over-weighted?
4. Which missing signal would have changed the decision?
5. Did the market fail, or did execution fail (creative, site, price, logistics, tracking, trust)?
6. Is the lesson specific to this product, or generalizable?
7. What rule change is proposed?
8. How much evidence supports that rule change?

## Rule-change governance

A single failed product should not automatically rewrite the scoring system.

Classify proposed lessons as:
- **observation** — interesting but insufficient evidence;
- **candidate rule** — repeated pattern worth monitoring;
- **validated rule** — enough repeated evidence to change the playbook;
- **retired rule** — formerly useful rule contradicted by later evidence.

Every scoring change should include:
- reason;
- affected dimensions;
- products supporting the change;
- products contradicting it;
- date;
- version / commit.

## Long-term calibration

Once the dataset is large enough, compare predicted probabilities with actual outcomes and measure which features correlate with winners. At that point, a simple statistical model may be more reliable than asking an LLM to invent new weights.

Fine-tuning should be considered only after memory, retrieval, structured scoring, and outcome calibration have been exploited.