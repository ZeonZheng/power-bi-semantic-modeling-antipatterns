# Power BI Semantic Modeling Anti-Patterns

A practical knowledge base and **deterministic negative-test kit** for intentionally designing low-quality Power BI semantic models to validate scanners, rule engines, and AI optimization workflows.

> [!WARNING]
> The patterns in this repository are intentionally bad designs. They are test fixtures and negative examples, **not production modeling recommendations**.

## Why this repository exists

A clean sample model is not enough to validate a semantic-model optimization scanner. The scanner needs realistic, controlled defects: poor schema design, unsafe relationships, weak date modeling, excessive model size, unnecessary calculated objects, confusing naming, and missing metadata.

This repository turns those defects into stable `AP-*` rules, model contracts, expected findings, clean controls, and evaluation utilities so scanner quality can be measured instead of judged subjectively.

## V1 at a glance

```text
Executable anti-pattern rules
          |
          v
  baseline-clean contract
          |
     controlled mutations
          v
    bad-basic contract
          |
   +------+-------+
   |              |
   v              v
expected       scanner
findings       findings
   |              |
   +------+-------+
          v
 precision / recall / F1
```

V1 currently defines **13 executable anti-patterns** across schema, relationships, dates, storage, calculations, and metadata.

## Repository structure

```text
.
├── docs/
│   ├── anti-pattern-catalog.md
│   ├── ai-generation-playbook.md
│   ├── model-quality-rubric.md
│   ├── references.md
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── examples/
│   └── bad-model-scenarios.md
├── manifests/
│   ├── baseline-clean.controls.yaml
│   └── bad-basic.expected.yaml
├── models/
│   ├── baseline-clean/
│   └── bad-basic/
├── prompts/
│   ├── generate-bad-semantic-model.md
│   └── generate-v1-retail-model.md
├── rules/
│   ├── antipattern-schema.json
│   └── antipatterns.yaml
├── specs/
│   ├── generation-contract.md
│   ├── scanner-result-contract.md
│   └── tmdl-mutation-spec.md
├── tests/
│   ├── conftest.py
│   ├── test_evaluate_scanner_results.py
│   └── test_validate_contracts.py
└── tools/
    ├── evaluate_scanner_results.py
    └── validate_contracts.py
```

## Core anti-pattern families

| Family | Typical defects intentionally introduced |
|---|---|
| Schema & grain | Flat mega-tables, mixed fact/dimension responsibilities, inconsistent fact grain, excessive snowflaking |
| Relationships | Fact-to-fact links, many-to-many shortcuts, unnecessary bidirectional filtering, ambiguous paths, 1:1 misuse |
| Date modeling | Missing or invalid date dimensions, auto date/time proliferation, poorly handled role-playing dates |
| Columns & storage | Unused columns, high-cardinality text/GUIDs, wrong data types, redundant data |
| Calculations | Avoidable calculated columns/tables, implicit aggregation, expensive or duplicated calculations |
| Naming & metadata | Technical/temporary names, exposed keys, missing descriptions, poor formatting and organization |

## Run the V1 contract checks

Python 3.10+ and PyYAML are required. `pytest` is required to run the tests.

```bash
python -m pip install pyyaml pytest
pytest -q
python tools/validate_contracts.py .
```

Expected validator result:

```text
Contract validation passed.
```

## Materialize the V1 Retail models

Use:

```text
prompts/generate-v1-retail-model.md
```

with an AI coding/modeling agent that can create PBIP/TMDL files. The agent is required to create the clean baseline first and derive `bad-basic` only through declared mutations.

The physical-model contract is documented in:

- `specs/generation-contract.md`
- `specs/tmdl-mutation-spec.md`

## Evaluate your scanner

Normalize scanner output to:

```json
{
  "findings": [
    {
      "id": "AP-REL-001",
      "object": "TEMP_Customer -> Sales_Final_v2",
      "severity": "Error"
    }
  ]
}
```

Then run:

```bash
python tools/evaluate_scanner_results.py \
  manifests/bad-basic.expected.yaml \
  actual-findings.json
```

The evaluator reports:

- true positives;
- false positives;
- false negatives;
- precision;
- recall;
- F1 score;
- severity mismatches;
- clean-control violations.

See `specs/scanner-result-contract.md` for exact matching semantics.

## Validation principle

A useful negative test model contains **deterministic, independently verifiable defects**. Avoid random corruption. Each injected defect should have:

- a stable anti-pattern ID;
- an expected severity;
- a concrete implementation recipe;
- a metadata/data signal a scanner can detect;
- a recommended production remediation;
- a ground-truth target object.

Some objects remain intentionally clean so false-positive behavior can also be measured.

## General scenario workflow

For scenarios beyond V1:

1. Pick a scenario from `examples/bad-model-scenarios.md`.
2. Select anti-pattern IDs from `docs/anti-pattern-catalog.md` / `rules/antipatterns.yaml`.
3. Use `prompts/generate-bad-semantic-model.md` to create a controlled negative fixture.
4. Generate an expected-findings manifest.
5. Scan the model.
6. Compare actual findings against ground truth.

## Scope

The repository focuses primarily on **semantic model design**. Power Query and report-layer anti-patterns are included only when they directly affect semantic-model quality, refresh cost, storage, or model behavior.

V1 does not deploy models to Power BI Service/Fabric and does not automate XMLA write-back. Physical PBIP/TMDL materialization is governed by the included generation contract and prompt.

## Reference basis

The catalog is derived primarily from Microsoft Power BI modeling guidance and the rule-based Best Practice Analyzer approach used by Tabular Editor. See `docs/references.md` for source links and mapping notes.
