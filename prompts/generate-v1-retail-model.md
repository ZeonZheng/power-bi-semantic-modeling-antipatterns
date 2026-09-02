# Prompt — Materialize the V1 Retail Anti-pattern Test Models

You are implementing deterministic negative-test fixtures for a Power BI semantic-model optimization scanner.

Your job is to create two technically valid PBIP/TMDL-compatible semantic models:

1. `baseline-clean` — the known-good control model;
2. `bad-basic` — derived from the baseline using exactly the declared V1 anti-pattern mutations.

These defects are test fixtures, not production recommendations.

## Read first

Treat the following repository files as authoritative, in this order:

1. `specs/generation-contract.md`
2. `rules/antipatterns.yaml`
3. `models/baseline-clean/model-manifest.yaml`
4. `manifests/baseline-clean.controls.yaml`
5. `models/bad-basic/model-manifest.yaml`
6. `manifests/bad-basic.expected.yaml`
7. `specs/tmdl-mutation-spec.md`

Do not invent additional anti-pattern IDs and do not silently fix declared defects.

## Target format

Create source-controlled semantic-model artifacts using TMDL. A valid PBIP wrapper may be added if the environment supports it.

Preferred output shape:

```text
<output-root>/
├── baseline-clean/
│   └── RetailBaselineClean.SemanticModel/
│       ├── definition/
│       │   ├── tables/
│       │   ├── relationships.tmdl
│       │   ├── model.tmdl
│       │   └── database.tmdl
│       └── definition.pbism
└── bad-basic/
    └── RetailBadBasic.SemanticModel/
        ├── definition/
        │   ├── tables/
        │   ├── relationships.tmdl
        │   ├── model.tmdl
        │   └── database.tmdl
        └── definition.pbism
```

## Phase A — baseline-clean

Materialize the baseline manifest first.

Required model shape:

```text
DimDate -----------+
DimCustomer -------+--> FactSales <-- DimProduct
DimStore ----------+
```

Requirements:

- 100,000 deterministic sales rows by default;
- 10,000 customers;
- 1,000 products;
- 50 stores;
- deterministic seed `20260902`;
- integer surrogate keys;
- single-direction 1:* relationships from dimensions to fact;
- dedicated marked Date table;
- hidden technical keys;
- explicit `[Net Sales]` measure;
- intentional currency format;
- descriptions for important semantic objects.

Before continuing, verify every entry in `manifests/baseline-clean.controls.yaml` is satisfied.

## Phase B — derive bad-basic

Copy/derive the clean model and apply exactly these V1 anti-pattern IDs:

```text
AP-SCH-001
AP-SCH-003
AP-REL-001
AP-DATE-001
AP-COL-001
AP-COL-002
AP-COL-003
AP-CALC-001
AP-CALC-003
AP-META-001
AP-META-002
AP-META-003
AP-META-005
```

Use `models/bad-basic/model-manifest.yaml` for exact target objects and `specs/tmdl-mutation-spec.md` for physical implementation guidance.

Key deterministic requirements include:

- `Sales_Final_v2[TransactionGUID]` is string with distinct ratio `>= 0.95`;
- `Sales_Final_v2[Freight]` repeats an order-header amount across order lines;
- `Sales_Final_v2[ProductKey]` contains numeric-looking values but is typed as string;
- `Sales_Final_v2[LineValue]` is a DAX calculated column using `[Quantity] * [UnitPrice]`;
- `TEMP_Customer -> Sales_Final_v2` uses bidirectional cross filtering;
- no dedicated `DimDate` remains in bad-basic;
- `[Net Sales]` and `DimStore[StoreKey]` remain intentionally clean controls.

## Phase C — ground-truth verification

Read every item in `manifests/bad-basic.expected.yaml` and verify:

```text
ID exists
+ canonical target object exists
+ evidence is materially present
= fixture is valid
```

Do not mark a rule complete based only on object naming when the evidence requires model metadata or generated data characteristics.

## Phase D — physical validity

Before finishing:

- parse/open the generated TMDL with the best compatible tool available in the environment;
- correct syntax or structural defects that are not declared anti-patterns;
- do not correct intentional anti-patterns;
- verify model relationships reference existing columns;
- verify DAX expressions reference existing objects;
- verify partitions/source expressions are syntactically valid;
- verify both semantic models remain scannable.

## Required completion report

Return a concise report containing:

```text
Baseline path:
Bad-basic path:
TMDL/PBIP validation method:
13/13 mutations present: yes/no
Clean controls preserved: yes/no
Unexpected defects found/fixed:
Remaining limitations:
```

If the environment cannot physically validate TMDL, state that explicitly rather than claiming the model is valid.
