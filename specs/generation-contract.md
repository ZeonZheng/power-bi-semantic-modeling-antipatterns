# V1 Model Generation Contract

This contract tells a human or AI implementation agent how to materialize the declarative V1 fixtures into PBIP/TMDL-compatible semantic-model artifacts.

## Source of truth

Read these files before creating model files:

1. `rules/antipatterns.yaml`
2. `models/baseline-clean/model-manifest.yaml`
3. `models/bad-basic/model-manifest.yaml`
4. `manifests/baseline-clean.controls.yaml`
5. `manifests/bad-basic.expected.yaml`
6. `specs/tmdl-mutation-spec.md`

Do not infer additional anti-patterns from names or examples. Only declared mutations are intentional V1 defects.

## Required generation order

### 1. Materialize baseline-clean

Create the clean model first. It must preserve the five-table Retail star schema, single-direction 1:* relationships, marked Date table, hidden technical keys, explicit `Net Sales` measure, descriptions, and formatting declared in the baseline manifest.

### 2. Validate the baseline conceptually

Before mutation, verify every object in `manifests/baseline-clean.controls.yaml` is still compliant. Do not proceed from a baseline that already contains a selected V1 anti-pattern.

### 3. Derive bad-basic

Create `bad-basic` from the baseline and apply only the mutations listed in `models/bad-basic/model-manifest.yaml`. Every mutation must retain its `AP-*` identity and canonical target object.

### 4. Preserve clean controls

Objects listed under `preserved_clean_controls` or `clean_controls` must remain compliant even though the surrounding model is intentionally degraded.

### 5. Verify ground truth

For each entry in `manifests/bad-basic.expected.yaml`, verify the target object exists and the declared evidence is materially present in the generated model or its deterministic synthetic data.

## Synthetic data defaults

Use deterministic data generation. Large committed CSV files are not required.

Default scale:

```yaml
sales_rows: 100000
customers: 10000
products: 1000
stores: 50
deterministic_seed: 20260902
```

The `TransactionGUID` defect must be real rather than name-based. Generate values so the distinct ratio is at least `0.95` at the default scale.

The mixed-grain defect must also be data-realistic: order-header `Freight` should repeat across multiple order-line rows for the same order.

## Physical artifact expectations

For a TMDL semantic model, prefer the normal source-controlled definition layout:

```text
<name>.SemanticModel/
├── definition/
│   ├── tables/
│   │   └── *.tmdl
│   ├── relationships.tmdl
│   ├── model.tmdl
│   └── database.tmdl
└── definition.pbism
```

A generator may use a valid PBIP project wrapper around this semantic-model folder. Do not commit binary PBIX as the primary V1 source artifact.

## Determinism requirements

Given the same manifest version and seed, a generator should produce equivalent:

- table/column/measure names;
- relationship topology;
- anti-pattern target objects;
- row-count scale;
- high-cardinality threshold behavior;
- expected-findings identity keys.

Lineage tags and generated GUID identifiers do not need to be byte-for-byte identical unless a specific generator requires stability.

## Safety boundary

These mutations are negative-test fixtures. Do not present them as recommended production modeling practices and do not silently repair them after generation.

## Acceptance checklist

A generated V1 fixture is acceptable only when:

- baseline-clean is openable/scannable;
- bad-basic is openable/scannable;
- all 13 declared V1 mutations are present;
- no undeclared parser corruption is introduced;
- canonical objects in the expected manifest exist;
- clean controls remain clean;
- `python tools/validate_contracts.py .` passes for the repository contracts.
