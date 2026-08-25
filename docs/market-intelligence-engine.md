# Market Intelligence Engine

## Mission

Build a continuously operating market-intelligence layer that searches for commercial asymmetries rather than periodically asking an LLM to find products.

TrendTrack is a particularly important input because its public API exposes programmable commerce signals including shop search, traffic/growth, active advertising, product catalogs, winning products, advertiser relationships and related intelligence surfaces.

## Architecture

```text
TrendTrack -----------+
Meta signals ---------+
Google Trends --------+
TikTok ---------------+
Reddit ---------------+--> Signal Normalizer --> Event Store --> Anomaly Engine
AliExpress -----------+                                      |
Search / marketplaces +                                      v
                                                        Investigation Queue
                                                              |
                                         +--------------------+--------------------+
                                         |                    |                    |
                                      Market                Social               Supply
                                      Agent                 Agent                Agent
                                         +--------------------+--------------------+
                                                              |
                                                        Analyst / Skeptic
                                                              |
                                                         Opportunity Score
```

## Event-driven research

Full research should not run continuously on every candidate.

Stage 1: cheap collection and deterministic calculations.

Stage 2: local-model classification and anomaly detection.

Stage 3: investigation only when thresholds are crossed.

Stage 4: frontier reasoning only for high-value ambiguity/disagreement.

## TrendTrack integration

Use TrendTrack as a primary structured discovery layer, not as an unquestioned source of truth.

Relevant capabilities include:
- shop discovery and advanced queries
- monthly visits and traffic growth
- active ads and ad-growth signals
- products and best sellers
- estimated revenue filters where exposed
- similar-shop discovery
- linked advertisers
- winning products
- ad creative/hook/landing-page intelligence
- tracked-brand monitoring

Cross-validation remains mandatory for consequential decisions.

## Signal Engine

Each raw observation becomes a normalized event.

Example:

```yaml
entity: product_or_store_id
source: trendtrack
signal: ads_growth
window: 7d
value: 4.8
observed_at: timestamp
reliability_weight: 0.85
```

Signals should be combined across sources rather than interpreted independently.

Potential composite dimensions:
- demand acceleration
- advertiser acceleration
- store traffic acceleration
- cross-store replication
- organic discussion velocity
- supplier availability
- margin potential
- saturation
- creative freshness
- geographic portability

## Business Genome

Represent observed stores using comparable structured features.

```text
STORE GENOME

Identity
├ category
├ geography
├ maturity
└ estimated scale

Acquisition DNA
├ Meta
├ TikTok
├ Google
└ organic

Creative DNA
├ hooks
├ angles
├ personas
├ formats
├ durations
└ CTAs

Offer DNA
├ price
├ discount
├ bundle
├ upsell
└ guarantee

Funnel DNA
├ landing structure
├ social proof
├ FAQ
├ checkout
└ post-purchase

Lifecycle DNA
├ email cadence
├ subjects
├ promotions
└ retention patterns
```

The long-term objective is pattern discovery across cohorts, not copying individual competitors.

## Market Pattern Discovery

Example candidate rule:

```text
Category: Home fitness
Sample: 31 scaling stores
Pattern:
  problem-first UGC
  + demonstration <7 sec
  + bundle x2
  + 30-day guarantee
Observed association: +27% scaling likelihood
Confidence: 0.74
```

This remains a hypothesis until tested against OH Ventures outcomes.

## Cross-source confirmation

A high-priority opportunity may look like:

```text
TrendTrack: scaling-store/product signal
            +
Meta: advertising activity accelerating
            +
Search/social: demand accelerating
            +
AliExpress: viable supply/margin
            +
Skeptic: no fatal contradiction
            =
High-priority investigation
```

## Opportunity investigation record

Every investigation should have a permanent ID and preserve pre-launch beliefs.

```text
INVESTIGATION-YYYY-MM-DD-XXXX

Market score
Demand score
Competition score
Supply score
Margin score
Creative potential
Operational complexity
Regulatory/IP risk
Bull thesis
Bear thesis
Final confidence
Decision
```

This record later becomes the input to the post-mortem.

## Prediction-to-outcome dataset

For every launched candidate preserve:

```text
Prediction
    ↓
Decision
    ↓
Execution configuration
    ↓
Traffic/ad spend
    ↓
CTR / CPC / CPA / CVR / AOV / ROAS
    ↓
Refunds / margin / LTV
    ↓
Post-mortem
```

This prediction-to-outcome history is expected to become one of OH Ventures' most valuable proprietary datasets.

## Portfolio learning

Knowledge can transfer between brands only when contextual similarity is sufficient.

Example:

```text
Brand A experiment succeeds
        ↓
Hermes identifies candidate transferable rule
        ↓
Similarity check against Brand C
        ↓
CRO experiment created
        ↓
Brand C validates / rejects
        ↓
OH Ventures rule confidence updates
```

## Market intelligence output

The system should optimize for exceptions, opportunities and decisions rather than raw data volume.

Example morning section:

```text
MARKET INTELLIGENCE

Stores observed: 12,481
New scaling signals: 37
Cross-validated candidates: 5
Full investigations triggered: 2

Top opportunity: #1821
Score: 92/100
Capital required for validation: €1,800
Bull/Bear disagreement: moderate
Recommended next action: controlled test
```

Numbers above are illustrative UI examples, not business forecasts.