# Anti-pattern Test Kit V1 Design

## Status

Approved in-chat concept, pending repository-spec review before implementation.

## Goal

Turn the current Power BI semantic-model anti-pattern knowledge base into a deterministic V1 test kit that can generate or materialize intentionally poor but technically valid semantic models and produce machine-readable ground truth for scanner validation.

## Scope

V1 is a vertical slice, not the complete benchmark suite. It covers:

1. executable anti-pattern definitions;
2. one clean Retail baseline model contract;
3. one intentionally degraded `bad-basic` model derived from that baseline;
4. expected-findings and clean-control manifests;
5. minimal validation and scanner-result scoring utilities;
6. documentation for AI-assisted PBIP/TMDL generation.

Out of scope for V1:

- all five/six benchmark variants;
- deployment to Power BI Service or Fabric;
- automated XMLA write-back;
- performance benchmarking orchestration;
- report generation;
- CI/CD deployment workflows.

## Design principles

### Deterministic defects

Each injected defect must map to one stable `AP-*` ID and a concrete semantic-model object/property. Random corruption is prohibited.

### Valid model first

The degraded model must remain syntactically and structurally valid enough to open, inspect, query, and scan. Parser-error testing is a separate concern and is not part of this V1.

### Clean baseline plus controlled mutations

The kit starts from a clean conceptual baseline. Anti-patterns are applied as mutations. This preserves a known-good reference and enables clean-control assertions for false-positive testing.

### Ground truth is first-class

Every generated bad model must ship with an expected-findings manifest containing the anti-pattern ID, target object, expected severity, and evidence. Clean controls are recorded separately.

### PBIP/TMDL-friendly

The executable contract must describe semantic objects and properties in a way an AI coding agent can map to PBIP/TMDL artifacts. The contract must not depend on a proprietary generator runtime.

## Target repository structure

```text
power-bi-semantic-modeling-antipatterns/
├── docs/
│   ├── anti-pattern-catalog.md
│   ├── ai-generation-playbook.md
│   ├── model-quality-rubric.md
│   ├── references.md
│   └── superpowers/
│       ├── specs/
│       │   └── 2026-09-02-antipattern-test-kit-v1-design.md
│       └── plans/
├── rules/
│   ├── antipatterns.yaml
│   └── antipattern-schema.json
├── specs/
│   ├── generation-contract.md
│   ├── tmdl-mutation-spec.md
│   └── scanner-result-contract.md
├── models/
│   ├── baseline-clean/
│   │   ├── model-manifest.yaml
│   │   └── README.md
│   └── bad-basic/
│       ├── model-manifest.yaml
│       └── README.md
├── manifests/
│   ├── baseline-clean.controls.yaml
│   └── bad-basic.expected.yaml
├── tools/
│   ├── validate_contracts.py
│   └── evaluate_scanner_results.py
├── tests/
│   ├── test_validate_contracts.py
│   └── test_evaluate_scanner_results.py
└── prompts/
    ├── generate-bad-semantic-model.md
    └── generate-v1-retail-model.md
```

## Executable anti-pattern contract

`rules/antipattern-schema.json` defines the machine-readable schema for each anti-pattern entry. Existing rules in `rules/antipatterns.yaml` will be extended gradually. V1 requires executable metadata for the anti-patterns used by `bad-basic`.

Required fields for executable V1 rules:

```yaml
id: AP-REL-001
family: relationships
name: Unnecessary Bidirectional Filtering
severity: Error
implementation:
  target_type: relationship
  preconditions:
    - dimension_to_fact_relationship_exists
  baseline:
    cross_filtering_behavior: oneDirection
  mutation:
    cross_filtering_behavior: bothDirections
expected_detection:
  object_type: Relationship
  evidence:
    cross_filtering_behavior: bothDirections
verification:
  method: metadata
  deterministic: true
```

The exact YAML shape is governed by `antipattern-schema.json` and documented in `specs/generation-contract.md`.

## V1 anti-pattern set

The `bad-basic` model will intentionally include the following rules because they span schema, relationships, dates, storage, calculations, and metadata without requiring advanced engine instrumentation:

- `AP-SCH-001` — Flat Mega Table
- `AP-SCH-003` — Inconsistent Fact Grain
- `AP-REL-001` — Unnecessary Bidirectional Filtering
- `AP-DATE-001` — No Proper Date Dimension
- `AP-COL-001` — High-Cardinality Text in Large Fact
- `AP-COL-002` — Unused Imported Columns
- `AP-COL-003` — Wrong Data Type
- `AP-CALC-001` — Avoidable Calculated Column
- `AP-CALC-003` — Implicit Measures Everywhere
- `AP-META-001` — Technical or Temporary Names
- `AP-META-002` — Exposed Technical Keys
- `AP-META-003` — Missing Descriptions
- `AP-META-005` — Inconsistent Formatting

## Clean Retail baseline contract

The conceptual baseline contains:

```text
DimDate -----------+
DimCustomer -------+--> FactSales <-- DimProduct
DimStore ----------+
```

Baseline requirements:

- `DimDate`, `DimCustomer`, `DimProduct`, `DimStore`, `FactSales`;
- integer surrogate keys;
- single-direction 1:* relationships from dimensions to fact;
- dedicated Date dimension;
- explicit `Net Sales` measure;
- hidden technical keys where appropriate;
- descriptions for important tables/measures;
- intentional format strings;
- no selected V1 anti-patterns.

The baseline is represented first as a model contract/manifest. V1 does not require binary PBIX storage.

## bad-basic mutation contract

The degraded model is derived from the baseline and must include deterministic changes such as:

- flatten customer/product/store descriptive attributes into a wide fact-like table;
- rename objects to examples such as `Sales_Final_v2`, `TEMP_Customer`, or `DimProductCopy`;
- repeat a header-grain amount across line-level rows;
- configure selected ordinary dimension-to-fact relationships as bidirectional;
- omit the dedicated Date dimension and use fact date columns directly;
- retain near-unique GUID/URL/comment text columns;
- store at least one numeric key as text;
- create a calculated `LineValue` column on the fact-like table;
- leave aggregatable numeric columns visible while providing few explicit measures;
- expose at least one technical key;
- leave selected descriptions blank;
- leave at least one business measure with default/inconsistent formatting.

The mutations must not introduce malformed TMDL/PBIP metadata.

## Synthetic data strategy

V1 avoids committing large datasets. The generation prompt/spec will instruct an implementation agent to use deterministic synthetic data generation, preferably Power Query M or a small generator script, with configurable row counts.

Recommended default scale for functional validation:

- Sales rows: 100,000
- Customers: 10,000
- Products: 1,000
- Stores: 50

High-cardinality columns should be generated so the expected distinct-ratio assertion is meaningful. Example: `TransactionGUID` distinct ratio >= 0.95.

The repository contract records thresholds; actual engine statistics are validated later when the physical model is materialized.

## Expected-findings manifest

`manifests/bad-basic.expected.yaml` is the ground truth for V1.

Each finding contains:

```yaml
- id: AP-COL-001
  severity: Warning
  object_type: column
  object: Sales_Final_v2[TransactionGUID]
  evidence:
    data_type: string
    expected_cardinality_ratio: ">=0.95"
```

The manifest also records clean controls:

```yaml
clean_controls:
  - object: DimStore[StoreKey]
    expectations:
      data_type: int64
      hidden: true
```

## Scanner result contract

`specs/scanner-result-contract.md` defines the normalized result shape consumed by the evaluator.

Minimum normalized finding fields:

```json
{
  "id": "AP-REL-001",
  "object": "TEMP_Customer -> Sales_Final_v2",
  "severity": "Error"
}
```

Matching is based primarily on anti-pattern ID plus canonical target object. Severity mismatch is reported separately and does not silently convert a finding into a different anti-pattern.

## Evaluation utility

`tools/evaluate_scanner_results.py` compares scanner output against the expected manifest and reports:

- true positives;
- false positives;
- false negatives;
- precision;
- recall;
- F1 score;
- severity mismatches;
- clean-control violations.

The utility must be deterministic and testable without Power BI/Fabric connectivity.

## Contract validation utility

`tools/validate_contracts.py` validates repository YAML/JSON artifacts before they are used by an agent or scanner test. It checks at minimum:

- duplicate anti-pattern IDs;
- referenced anti-pattern IDs exist;
- expected manifest objects are non-empty;
- required executable implementation fields exist for V1 rules;
- clean-control entries are structurally valid.

No Fabric/Power BI SDK is required for this utility.

## Testing strategy

Implementation follows test-driven development for the Python utilities.

Required test categories:

1. valid contracts pass;
2. unknown anti-pattern IDs fail validation;
3. duplicate IDs fail validation;
4. evaluator computes exact TP/FP/FN counts;
5. evaluator computes precision/recall/F1 correctly;
6. severity mismatches are surfaced;
7. clean-control violations are surfaced;
8. empty expected/actual sets do not cause division errors.

Model/TMDL physical validation is a later integration layer. V1 repository tests focus on the deterministic contracts and evaluator.

## AI generation prompt

`prompts/generate-v1-retail-model.md` instructs an AI coding/modeling agent to:

1. read the generation contract and V1 rules;
2. materialize the baseline model in PBIP/TMDL-compatible form;
3. derive `bad-basic` only through declared mutations;
4. generate deterministic synthetic data;
5. preserve clean controls;
6. emit or verify the expected-findings manifest;
7. verify that the generated model remains syntactically valid;
8. avoid fixing intentionally injected defects.

## Data flow

```text
rules/antipatterns.yaml
        |
        v
Executable rule contract
        |
        +--------------------+
        |                    |
        v                    v
baseline-clean          bad-basic mutations
        |                    |
        +---------+----------+
                  v
          physical PBIP/TMDL
                  |
        +---------+----------+
        |                    |
        v                    v
expected manifest       scanner output
        |                    |
        +---------+----------+
                  v
       evaluate_scanner_results.py
                  |
                  v
       precision / recall / F1
```

## Success criteria

V1 is complete when:

- the selected 13 anti-patterns have executable contract metadata;
- all repository contracts validate;
- baseline and bad-basic manifests exist and are internally consistent;
- a reusable AI prompt can materialize the two models from the contracts;
- evaluator tests pass for TP/FP/FN, severity mismatch, and clean controls;
- README documents the V1 workflow;
- no Power BI/Fabric credentials are required to run contract validation and scoring locally.

## Future extensions

After V1 is validated with the existing semantic-model optimization scanner, expand using the same contracts to:

- `bad-relationships`;
- `bad-storage`;
- `bad-metadata`;
- `bad-mixed-benchmark`;
- physical PBIP/TMDL fixtures committed where practical;
- VertiPaq/statistics assertions;
- automated deployment and scan orchestration.
