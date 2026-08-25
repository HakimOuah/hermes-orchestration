# Product Research System

## Objective

Increase the probability of selecting profitable products by combining strict research criteria, broad evidence collection, cheap local execution, frontier-model review, and post-launch learning.

## Workflow

### 1. Human request
The user expresses the business intent naturally: target market, price range, constraints, category preferences, risk tolerance, and any current hypotheses.

### 2. Frontier policy pass
A frontier model converts that intent into a strict research brief containing:
- hard constraints;
- immediate rejection criteria;
- required sources;
- scoring dimensions;
- minimum evidence requirements;
- uncertainties that must be surfaced;
- expected output format.

The frontier model should define the method, not spend expensive tokens performing every search.

### 3. Hermes orchestration
Hermes creates a mission ID, assigns local agents, controls tools, logs sources, enforces budgets, and stores intermediate results.

### 4. Local research
The local researcher explores relevant sources such as:
- TrendTrack or equivalent product intelligence tools;
- web search;
- search demand / SEO data;
- Google Trends;
- Meta Ad Library / visible ad signals;
- marketplaces;
- Reddit / forums / customer reviews;
- suppliers / AliExpress APIs;
- competitor sites.

Available sources will depend on tool access and current integrations.

### 5. Funnel candidates
A typical funnel may be:

```text
200 raw candidates
 -> 40 plausible candidates
 -> 10 researched candidates
 -> 5 deep dives
 -> 3 finalists
```

Exact numbers are not important. The key principle is that expensive models see only the smallest useful shortlist.

### 6. Evidence pack
Each finalist should include:
- thesis;
- target customer problem;
- demand evidence;
- competitor landscape;
- pricing and margin assumptions;
- differentiation potential;
- creative/visual potential;
- customer objections;
- operational/logistics risks;
- GMC/policy risks;
- contrary evidence;
- confidence by dimension;
- unknowns requiring validation.

### 7. Adversarial frontier audit
The final frontier reviewer receives the shortlist with a deliberately skeptical mission:

> Find the strongest reasons each recommendation could fail. Identify weak evidence, hidden assumptions, false positives, and missing market signals. Do not reward consensus.

### 8. Human decision
The system recommends GO / HOLD / NO-GO with rationale. The final launch decision remains human.

## Example mission schema

```yaml
mission_id: PR-YYYY-NNN
market: FR
price_range_eur: [150, 300]
net_margin_target_pct: 20
hard_constraints:
  - GMC compatible without relying on prohibited claims
  - credible consumer problem or desire
  - viable supplier economics
reject_if:
  - trademark/IP dependency
  - unsustainable race-to-bottom pricing
  - economics require unrealistic CVR
required_output:
  shortlist_size: 3
  evidence_pack: true
  contrary_evidence: true
  confidence_scores: true
```

This is a template only. Actual criteria should come from the existing product-research documentation and be calibrated from outcomes.