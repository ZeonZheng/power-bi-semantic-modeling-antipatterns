# AI Generation Playbook

This playbook tells an AI agent how to create intentionally poor Power BI semantic models in a controlled, testable way.

## Objective

Generate a semantic model that is **bad by design but still technically loadable and analyzable**. The goal is not random corruption. The goal is to create realistic modeling defects that a semantic-model scanner should detect.

## Core rules for the AI

1. **Keep the model valid enough to open and scan.**
   - Avoid malformed metadata that prevents the model from loading.
   - Avoid deliberately breaking every relationship or expression.

2. **Inject explicit anti-pattern IDs.**
   - Every intentional defect must map to an ID from `docs/anti-pattern-catalog.md`.
   - Record the injected IDs in an expected-findings manifest.

3. **Prefer realistic mistakes over absurd ones.**
   - Use patterns a developer could plausibly create under time pressure.
   - Examples: bidirectional relationships everywhere, duplicated dimensions, technical object names, unused high-cardinality columns.

4. **Create independent test signals.**
   - Do not make every problem depend on one root cause.
   - A scanner should be able to detect relationship, storage, metadata, and calculation issues independently.

5. **Do not accidentally optimize the model.**
   - Do not automatically remove redundant columns.
   - Do not normalize naming unless explicitly requested.
   - Do not replace many-to-many relationships with bridges.
   - Do not create descriptions or display folders unless the scenario asks for a mixed-quality model.

6. **Preserve semantic correctness where needed.**
   - Some anti-patterns should be inefficient or confusing rather than completely wrong.
   - Keep enough measures working to allow performance testing.

## Recommended generation workflow

### Step 1 — Start from a plausible dataset

Good test domains:
- retail sales;
- orders and shipments;
- finance transactions;
- service tickets;
- manufacturing production;
- inventory and procurement.

Prefer datasets with:
- at least one large transaction table;
- several descriptive entities;
- multiple date roles;
- numeric measures;
- some high-cardinality identifiers/text.

### Step 2 — Define a clean conceptual baseline

Before making the model bad, identify the clean design that would normally be expected.

Example:

```text
DimDate -----------+
DimCustomer -------+--> FactSales <-- DimProduct
DimGeography ------+
```

This gives a reference against which intentional degradation can be measured.

### Step 3 — Select anti-patterns

Choose a controlled set, for example:

```text
AP-SCH-001
AP-SCH-003
AP-REL-001
AP-REL-002
AP-REL-003
AP-DATE-001
AP-COL-001
AP-COL-002
AP-CALC-001
AP-CALC-003
AP-META-001
AP-META-002
AP-META-003
```

### Step 4 — Apply degradation deliberately

For each selected ID, make one or more concrete changes.

Example transformation:

```text
Clean design:
DimCustomer --> FactSales <-- DimProduct

Bad design:
Customer attributes copied into FactSales
Product attributes copied into FactSales
FactSales <--> FactReturns
Customer <--> FactSales (Both)
FactSales <--> Product (Both)
```

### Step 5 — Produce an expected-findings manifest

The AI must output something similar to:

```yaml
scenario: retail-bad-model-01
expected_findings:
  - id: AP-SCH-001
    object: FactSales
    evidence: Customer and Product descriptive attributes duplicated into large fact table
  - id: AP-REL-001
    object: DimCustomer -> FactSales
    evidence: Cross-filter direction set to Both
  - id: AP-META-001
    object: TEMP_ProductCopy
    evidence: Temporary technical naming pattern
```

This becomes the scanner's expected result set.

## Difficulty levels

### Level 1 — Obvious
Use highly visible, deterministic defects.

Examples:
- `TEMP_`/`Copy` names;
- exposed key columns;
- no descriptions;
- bidirectional relationships;
- large unused text fields.

Best for initial scanner functional testing.

### Level 2 — Realistic
Use defects that require metadata context.

Examples:
- inconsistent fact grain;
- duplicate dimensions;
- inappropriate many-to-many relationships;
- avoidable calculated columns;
- missing explicit measures.

Best for rule-quality testing.

### Level 3 — Subtle
Use patterns that require dependency or graph analysis.

Examples:
- duplicated DAX logic;
- ambiguous relationship paths;
- role-playing date misuse;
- ineffective security topology;
- high-cardinality columns whose impact depends on table size.

Best for mature scanner evaluation.

## Anti-pattern density

Avoid making every object bad. A useful test model needs both positive and negative controls.

Suggested ratio:

```text
70% deliberately problematic objects
30% reasonably modeled objects
```

This helps test false-positive behavior.

## Naming strategy for intentionally poor objects

Use a mixture of realistic weak names:

```text
Table1
Query2
Sales_Final_v2
STG_Order
TEMP_Customer
DimCustomerCopy
newtable
col1
Measure 7
Total2
Revenue_test
```

Do not use the exact same prefix everywhere; otherwise the scanner can appear accurate through a trivial naming heuristic.

## Required output from an AI generation task

Every generated bad model should be accompanied by:

1. **Scenario description**
2. **Selected anti-pattern IDs**
3. **Object-by-object change list**
4. **Expected-findings manifest**
5. **Clean-design comparison**
6. **Known intentionally clean objects**
7. **Any anti-patterns that could not be implemented**

## What the AI must not do

Do not:
- introduce syntax errors solely to make the model fail;
- corrupt PBIX/TMDL metadata;
- create invalid DAX unless testing syntax validation specifically;
- remove all relationships;
- create impossible cardinality metadata;
- use random defects without recording them;
- claim an anti-pattern was injected without evidence.

The model should be **poorly engineered, not unusable**.
