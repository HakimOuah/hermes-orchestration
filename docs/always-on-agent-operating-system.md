# Always-On Agent Operating System

## Vision

The Mac mini + Hermes stack should evolve beyond a product-research machine into an **always-on operating system for OH Ventures**.

The key question is not only:

> What tasks can Hermes execute?

It is:

> What phenomena in the business deserve to be observed continuously?

The target loop is:

```text
Observe -> Detect -> Understand -> Act -> Measure -> Learn
```

Most continuous monitoring, extraction, classification, cleanup and scoring should run on local models. Frontier models should be escalated to when uncertainty, business impact, strategic reasoning or audit requirements justify their cost.

## Agent families

### 1. Builders

Agents that create and maintain software.

Typical responsibilities:
- implement GitHub issues
- frontend/backend development
- run tests and linting
- inspect screenshots
- fix failures
- review code
- prepare pull requests

Long-term loop:

```text
Issue -> Code -> Test -> Review -> Fix -> Human approval
```

### 2. Watchers

Mostly idle agents whose job is continuous observation.

Examples:
- repository health
- CI failures
- dependency/security alerts
- analytics anomalies
- ranking changes
- competitor changes
- product/trend signals

They should trigger expensive downstream analysis only when a meaningful event occurs.

### 3. Researchers

Agents that continuously build structured knowledge rather than merely generating one-off summaries.

Possible sources:
- X
- GitHub
- Hacker News
- research papers
- AI/model releases
- industry blogs
- Reddit
- market and competitor sources

Their output should feed persistent, queryable knowledge rather than disappear after each run.

### 4. Experimenters

Agents that benchmark models, prompts, workflows and business hypotheses.

This connects directly to HakimBench: benchmark models on real OH Ventures tasks rather than relying primarily on public benchmarks.

Track:
- task success
- quality
- latency
- token/API cost
- human corrections
- failure modes

### 5. Workers

High-volume, low-risk repetitive execution:
- extraction
- normalization
- classification
- file organization
- deduplication
- enrichment
- scoring
- translation
- summarization

This is a primary use case for inexpensive local inference.

### 6. Managers

Higher-level agents that inspect state, prioritize work and dispatch specialist agents.

Example objective:

```text
Maintain OH Ventures projects in good operational health.
```

A manager may detect a SponsorAI bug and dispatch a coding agent, detect a Shopify conversion anomaly and dispatch an analytics agent, or detect a market opportunity and dispatch the product-research pipeline.

## OH Ventures agent portfolio

### Opportunity Radar

Continuously monitor market signals across sources such as TikTok, X, Reddit, Google Trends, Meta advertising, marketplaces, AliExpress and Shopify ecosystems.

Do not perform full product research on everything. Detect anomalies and emerging correlations first.

Example signal object:

```text
Product / category
Reddit mentions: +140%
TikTok velocity: +80%
Advertiser count: +35%
Search demand: +22%
Supplier/order signal: +18%
```

Only high-signal candidates should trigger the expensive product-research workflow.

### Competitor Intelligence Agent

Maintain a longitudinal competitor database.

Track:
- products
- prices
- promotions
- bundles
- landing pages
- creatives
- advertising activity
- reviews
- new launches

Important events include rapid creative scaling and several unrelated stores launching the same product/category within a short period.

### Business Analyst

Nightly ingestion from relevant commerce, advertising, payment and analytics systems.

Track metrics such as:
- revenue
- contribution margin
- CAC
- ROAS
- conversion rate
- AOV
- refunds
- chargebacks
- inventory

The primary goal is anomaly detection and diagnosis, not dashboard duplication.

Desired loop:

```text
Detect -> Diagnose -> Dispatch fix -> Measure recovery
```

### CRO Scientist

Maintain a backlog of conversion hypotheses and experimental results.

For each experiment store:
- hypothesis
- expected impact
- confidence
- implementation
- result
- segment/device effects
- conclusion
- reusable learned rule

Over time this should create an OH Ventures-specific CRO knowledge base.

### Creative Intelligence Agent

Analyze advertising performance against creative attributes.

Possible dimensions:
- hook
- angle
- format
- UGC style
- duration
- CTA
- visual structure
- persona
- CTR
- CPA
- ROAS

The purpose is to discover reusable relationships between creative patterns, audiences and commercial outcomes, then feed those learned rules back into creative generation.

### Customer Intelligence Agent

Continuously classify customer evidence from reviews, emails, support tickets, returns, ad comments and public discussions.

Extract:
- objections
- pain points
- desired outcomes
- recurring questions
- product complaints
- language customers actually use

Feed validated insights into copywriting, PDPs, FAQs, product development and advertising angles.

### SEO / GEO Watcher

Monitor:
- rankings
- Search Console
- competitors
- SERP changes
- AI/answer-engine visibility
- indexation
- technical errors
- content decay

On a meaningful loss, diagnose the likely cause, compare competitors and prepare a recommended intervention or code/content change for approval.

### CEO Briefing Agent

The human should not need to communicate with every specialist agent.

Hermes should aggregate important events into a concise executive briefing.

Example:

```text
OH VENTURES — MORNING BRIEF

BUSINESS
Revenue yesterday: ...
Trend vs 7d: ...

ALERTS
Store X mobile CVR: -21%
Likely cause: ...

OPPORTUNITIES
Candidate Y: 87/100
Why it surfaced: ...

CREATIVE
Winning angle: ...

EXPERIMENTS
Test #38 completed
Result: +11.2% CVR

AGENTS
Tasks completed: ...
Escalated: ...
Human decisions required: ...
```

The CEO briefing should optimize for decisions, exceptions and opportunities — not activity logs.

## Target orchestration

```text
                         Human
                           |
                           v
                        Hermes
                    Orchestrator
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
       Watchers          Workers        Researchers
          |                |                |
          +-------- Local open models ------+
                           |
                    confidence / risk gate
                           |
                           v
                    Frontier models
             strategy / audit / hard reasoning
                           |
                           v
                    Human approval gate
```

## Core economic principle

Do not use frontier intelligence merely because it is available.

Use local models for large quantities of inexpensive cognition:
- observe
- classify
- extract
- summarize
- compare
- clean
- score

Escalate when the expected value of better reasoning exceeds the API/model cost or when the action has material business consequences.

## Proprietary memory as moat

The long-term asset is not the number of agents or the model running them. It is the accumulated operational dataset.

Examples:
- products rejected and why
- predictions made before launches
- actual launch outcomes
- winning/losing hooks
- landing-page experiments
- supplier reliability
- recurring customer objections
- leading indicators of revenue changes
- model performance on real tasks
- human overrides and their outcomes

This creates a proprietary decision history that generic models do not possess.

## Design principle for H24 agents

An always-on agent does not need to generate output continuously.

The preferred pattern is:

```text
Cheap continuous observation
        |
meaningful event detected?
   no -> sleep / continue
   yes
        v
local analysis
        |
confidence / impact gate
        |
frontier analysis if justified
        |
action or human decision
        |
measure outcome
        |
update memory
```

This event-driven design should be preferred over blindly running expensive reasoning loops 24/7.

## Future extensions beyond e-commerce

The same architecture should later be adapted to:
- SponsorAI prospecting, campaign intelligence and follow-up
- software/project maintenance across repositories
- personal/work knowledge management
- AI/technology intelligence to reduce dependence on manually browsing X

These should reuse the same primitives: watchers, workers, researchers, managers, memory, escalation and feedback loops.
