# Power BI Semantic Modeling Anti-Patterns

A practical knowledge base for **intentionally designing low-quality Power BI semantic models** for scanner, rule-engine, and AI validation.

> [!WARNING]
> The patterns in this repository are intentionally bad designs. They are test fixtures and negative examples, **not production modeling recommendations**.

## Why this repository exists

When validating a semantic-model optimization scanner, a clean sample model is not enough. The scanner needs models containing realistic mistakes that Power BI developers commonly make: poor schema design, unsafe relationships, weak date modeling, excessive model size, unnecessary calculated objects, confusing naming, and missing metadata.

This repository converts those mistakes into a repeatable anti-pattern catalog that can be consumed by humans or AI agents to generate deliberately poor test models.

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── anti-pattern-catalog.md
│   ├── ai-generation-playbook.md
│   ├── model-quality-rubric.md
│   └── references.md
├── examples/
│   └── bad-model-scenarios.md
├── prompts/
│   └── generate-bad-semantic-model.md
└── rules/
    └── antipatterns.yaml
```

## Core anti-pattern families

| Family | Typical defects intentionally introduced |
|---|---|
| Schema & grain | Flat mega-tables, mixed fact/dimension responsibilities, inconsistent fact grain, excessive snowflaking |
| Relationships | Fact-to-fact links, many-to-many shortcuts, unnecessary bidirectional filtering, ambiguous paths, 1:1 misuse |
| Date modeling | Missing or invalid date dimensions, auto date/time proliferation, poorly handled role-playing dates |
| Columns & storage | Unused columns, high-cardinality text/GUIDs, wrong data types, redundant data, inappropriate storage choices |
| Calculations | Avoidable calculated columns/tables, implicit aggregation, expensive or duplicated calculations |
| Naming & metadata | Technical/temporary names, exposed keys, missing descriptions, poor formatting and organization |

## How to use it

1. Pick a scenario from `examples/bad-model-scenarios.md`.
2. Select the anti-pattern IDs you want to inject from `docs/anti-pattern-catalog.md`.
3. Give `prompts/generate-bad-semantic-model.md` plus the selected IDs to an AI coding/modeling agent.
4. Build the intentionally bad semantic model.
5. Scan it with your optimization solution.
6. Compare detected issues against the expected anti-pattern manifest.

For automated generation, `rules/antipatterns.yaml` provides a machine-readable form of the catalog.

## Validation principle

A useful negative test model should contain **deterministic, independently verifiable defects**. Avoid random corruption. Each injected defect should have:

- a stable anti-pattern ID;
- an expected severity;
- a concrete implementation recipe;
- a metadata or behavioral signal a scanner can detect;
- a recommended production remediation.

This makes the model suitable for precision/recall testing instead of subjective visual review.

## Scope

This repository focuses primarily on **semantic model design**. Power Query and report-layer anti-patterns are included only when they directly affect semantic-model quality, refresh cost, storage, or model behavior.

## Reference basis

The catalog is derived primarily from Microsoft Power BI modeling guidance and the rule-based Best Practice Analyzer approach used by Tabular Editor. See `docs/references.md` for source links and mapping notes.
