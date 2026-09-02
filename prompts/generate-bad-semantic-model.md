# Reusable Prompt — Generate an Intentionally Poor Power BI Semantic Model

Use the prompt below with an AI coding/modeling agent.

---

You are creating a **negative-test Power BI semantic model** for validating a semantic-model optimization scanner.

The model must be intentionally poorly designed, but it must remain technically valid, loadable, and analyzable. Do not create random corruption or invalid metadata.

## Inputs

- Dataset/domain: `<describe dataset>`
- Desired difficulty: `<Level 1 | Level 2 | Level 3>`
- Selected anti-pattern IDs: `<list IDs from docs/anti-pattern-catalog.md>`
- Target model format/tooling: `<PBIP/TMDL/Tabular Editor/Fabric semantic model/etc.>`

## Requirements

1. Read the selected anti-pattern definitions before changing the model.
2. Establish what a clean star-schema-oriented design would look like first.
3. Intentionally degrade the model only according to the selected anti-pattern IDs.
4. Preserve enough valid relationships, measures, and data for scanning and query/performance testing.
5. Include realistic developer mistakes rather than arbitrary damage.
6. Keep some objects intentionally clean so false-positive behavior can be tested.
7. Do not silently fix anti-patterns after creating them.
8. Do not introduce syntax errors or malformed semantic-model metadata unless explicitly asked to test parser/error handling.

## Required deliverables

Produce:

### A. Clean conceptual baseline

Show the model shape that would normally be recommended.

### B. Degradation plan

For every selected anti-pattern ID, provide:

```text
Anti-pattern ID:
Target object(s):
Exact change:
Why this creates the anti-pattern:
Expected scanner signal:
```

### C. Implemented model

Create or modify the semantic-model files/artifacts using the requested tooling.

### D. Expected-findings manifest

Create a machine-readable manifest similar to:

```yaml
scenario: <name>
expected_findings:
  - id: AP-REL-001
    severity: Error
    object: DimCustomer -> FactSales
    evidence: Cross-filter direction is Both
  - id: AP-COL-001
    severity: Warning
    object: FactSales[TransactionGUID]
    evidence: High-cardinality text column retained in large imported fact table
clean_controls:
  - object: DimStore[StoreKey]
    expectation: Compact integer key, hidden, valid single-direction relationship
```

### E. Verification

Before finishing, verify:

- the model can still be opened/scanned;
- selected anti-patterns actually exist;
- expected findings correspond to concrete metadata/expressions;
- clean controls remain clean;
- no unrequested corruption was introduced.

## Important constraint

These defects are for controlled scanner testing only. Do not present them as production best practices.
