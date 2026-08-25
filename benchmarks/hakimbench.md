# HakimBench

## Purpose
Public leaderboards are weak proxies for the real job. HakimBench will evaluate models on the actual e-commerce tasks this system needs.

## When to run
Run the first full benchmark after the Mac mini is available and the current generation of local models has been selected.

## Candidate models
Benchmark at least:
- the strongest local model that fits comfortably;
- one alternative local model with different architecture/training;
- one low-cost API model;
- one frontier GPT-class model;
- one frontier Claude-class model.

Do not assume today's model shortlist will still be optimal in six weeks.

## Proposed tasks
1. Product candidate triage
2. GO / NO-GO product analysis
3. Competitor landscape synthesis
4. Identification of a real positioning gap
5. Customer review mining
6. Pain/desire intensity analysis
7. Offer construction
8. Pricing/margin reasoning
9. Risk identification
10. Ad angle generation
11. Hero section / PDP copy draft
12. Copywriting audit
13. GMC-oriented pre-audit
14. SEO/content structure
15. Evidence-vs-inference discipline
16. Adversarial critique of another model's recommendation
17. Long-context synthesis across many sources
18. Tool-call reliability under Hermes
19. French writing quality
20. Cost / latency / memory footprint

## Scoring dimensions

Each task should be scored blind where possible on:
- business judgment;
- logical reasoning;
- evidence discipline;
- originality without hallucination;
- marketing quality;
- actionability;
- instruction following;
- tool reliability;
- speed;
- cost.

## Key output
The goal is not to crown a universal winner. The benchmark should produce a routing map such as:

```text
Product triage           -> local model A
Review mining            -> local model A
Competitor strategy      -> API model B
Premium copy audit       -> frontier model C
Final product challenge  -> frontier model D
```

## Benchmark hygiene
Use identical input packs, separate model outputs from evaluator identities, and record model version, quantization, reasoning settings, context length, runtime and cost.