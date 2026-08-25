# Model Routing

## Objective

Route each task to the cheapest model class that can perform it reliably, while reserving frontier models for high-value reasoning and audits.

## Tier 0 — Local models

Primary use cases:
- product candidate triage;
- competitor extraction and synthesis;
- review mining;
- SEO drafts;
- translation;
- FAQ and PDP drafts;
- classification and scoring;
- data cleanup;
- repeated iterations;
- preparation of evidence packs for stronger models.

Initial candidates to benchmark when hardware arrives:
- current Qwen 3.5 variants that fit comfortably in 48 GB unified memory;
- GPT-OSS 20B;
- any newer open-weight models available at that date.

Do not freeze the stack now. Re-evaluate open-weight releases immediately before implementation.

## Tier 1 — Low-cost API models

Use for:
- deeper market analysis;
- independent second opinions;
- larger-context synthesis;
- tasks where the local model is uncertain or inconsistent.

Candidate families should be selected based on current price/performance at implementation time, e.g. GLM, Kimi, MiniMax or successors.

## Tier 2 — Frontier APIs

Use for:
- final GO / NO-GO challenges;
- premium copywriting audits;
- strategic positioning;
- difficult reasoning;
- final critical GMC/compliance review;
- adversarial analysis of shortlisted products.

Likely candidates: the strongest available GPT / Claude-class models at the time of execution.

## Tier 3 — Human decision

Mandatory approval for:
- committing meaningful ad spend;
- supplier orders / stock commitments;
- final launch decisions;
- any policy-sensitive or legally consequential publication;
- changes to core scoring weights that lack enough evidence.

## Routing rules

A task should escalate when one or more conditions apply:
- local confidence is low;
- evidence is contradictory;
- the decision has high financial impact;
- the output is customer-facing and high leverage;
- a second independent reasoning path is valuable;
- a policy/compliance risk exists;
- the local model repeatedly fails the same evaluation criterion.

## Preferred pattern

```text
Local execution
   -> local self-check
   -> low-cost API second opinion if needed
   -> frontier adversarial audit for final shortlist
   -> human approval
```

The frontier model should often receive a compact evidence pack rather than the raw research corpus. This minimizes API cost and forces the local layer to do the bulk of the work.