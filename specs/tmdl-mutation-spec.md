# TMDL Mutation Specification — V1

This document maps the declarative V1 mutations to Tabular Object Model/TMDL concepts. It is an implementation guide, not a replacement for `rules/antipatterns.yaml`.

Microsoft documents TMDL as a text representation of the Tabular Object Model (TOM); TMDL objects expose TOM properties. A source-controlled semantic model commonly stores table definitions under `definition/tables/*.tmdl` and relationships in `definition/relationships.tmdl`.

## Canonical object notation

| Object type | Manifest notation | Physical interpretation |
|---|---|---|
| Table | `Sales_Final_v2` | TMDL `table` object |
| Column | `Sales_Final_v2[ProductKey]` | column under the named table |
| Measure | `[Total Sales Raw]` | measure; table location is secondary to the V1 identity key |
| Relationship | `TEMP_Customer -> Sales_Final_v2` | relationship connecting the named tables |
| Model | `Model` | model-level structure/property |

## Relevant TMDL patterns

A normal imported column can be represented with properties such as `dataType`, `isHidden`, `sourceColumn`, and `summarizeBy`. Measures use a DAX expression and can declare `formatString`. Calculated columns use the column declaration's default expression, for example conceptually:

```tmdl
table Sales_Final_v2
    column LineValue = [Quantity] * [UnitPrice]
        dataType: decimal
        summarizeBy: sum
```

Relationships identify `fromColumn` and `toColumn`; TOM/TMDL relationship properties also include cross-filtering behavior. For the bidirectional negative fixture, the physical relationship must resolve to the TOM value `BothDirections` / TMDL value `bothDirections` rather than the baseline `OneDirection` / `oneDirection` behavior.

## V1 mutation mapping

### AP-SCH-001 — Flat Mega Table

- Start from separated Customer/Product/Store descriptive attributes.
- Move/copy selected descriptive attributes into `Sales_Final_v2`.
- The fact-like table must remain high-row-count.
- Keep `DimStore` sufficiently intact to preserve its clean control.

### AP-SCH-003 — Inconsistent Fact Grain

- Keep the fact grain at order-line level.
- Add `Sales_Final_v2[Freight]` as an order-header value repeated on each line of an order.
- The repeated value must be observable in generated data, not merely documented.

### AP-REL-001 — Unnecessary Bidirectional Filtering

Baseline relationship concept:

```text
TEMP_Customer (1) -> Sales_Final_v2 (*)
cross filtering: oneDirection
```

Mutation:

```text
crossFilteringBehavior: bothDirections
```

Do not create an invalid ambiguous graph merely to satisfy this rule; this V1 defect is the relationship direction itself.

### AP-DATE-001 — No Proper Date Dimension

- Remove/omit the dedicated `DimDate` table from bad-basic.
- Remove its relationship to the fact.
- Retain and expose `Sales_Final_v2[OrderDate]` for direct date analysis.

### AP-COL-001 — High-Cardinality Text in Large Fact

- Create `Sales_Final_v2[TransactionGUID]` as `string`.
- Generate deterministic near-unique values with distinct ratio `>= 0.95`.
- Keep the column in the imported fact-like table.

### AP-COL-002 — Unused Imported Columns

- Add/import `Sales_Final_v2[LoadTimestamp]`.
- Do not reference it from relationships, measures, hierarchies, sort-by properties, or other analytical dependencies.

### AP-COL-003 — Wrong Data Type

Baseline:

```tmdl
column ProductKey
    dataType: int64
```

Mutation:

```tmdl
column ProductKey
    dataType: string
```

The generated values should still be numeric-looking keys so a scanner can infer semantic mismatch.

### AP-CALC-001 — Avoidable Calculated Column

Materialize `Sales_Final_v2[LineValue]` as a DAX calculated column using the row expression `[Quantity] * [UnitPrice]` instead of leaving the logic solely upstream or as an explicit measure.

### AP-CALC-003 — Implicit Measures Everywhere

- Keep raw numeric fact columns such as `SalesAmount` visible and aggregatable.
- Provide intentionally few explicit measures.
- Preserve `[Net Sales]` as a clean control; the defect is model-wide reliance on exposed raw numeric columns, not the total absence of measures.

### AP-META-001 — Technical or Temporary Names

Use the declared names exactly where practical:

- `Sales_Final_v2`
- `TEMP_Customer`
- `DimProductCopy`

Do not rename the clean-control `DimStore` merely to increase issue count.

### AP-META-002 — Exposed Technical Keys

For `Sales_Final_v2[CustomerKey]`, omit/remove the `isHidden` flag so the relationship-only key is visible.

### AP-META-003 — Missing Descriptions

TMDL supports object descriptions. For the target `Sales_Final_v2`, omit the description documentation that is present on the clean baseline's important objects.

### AP-META-005 — Inconsistent Formatting

Create `[Total Sales Raw]` as a business measure with default/general formatting, for example:

```tmdl
measure 'Total Sales Raw' = SUM(Sales_Final_v2[SalesAmount])
    formatString: General
```

Keep `[Net Sales]` intentionally well-formatted as a clean control.

## Physical validation notes

The generated artifacts should be parsed/opened by a compatible Power BI/TMDL tool before being treated as a valid scanner fixture. Contract validation in this repository checks consistency of the declarative ground truth; it does not claim to parse every TMDL grammar rule.

## Microsoft references

- TMDL overview: https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview
- TMDL object definitions: https://learn.microsoft.com/analysis-services/tmdl/tmdl-reference-tabular-object
- Fabric semantic model definition structure: https://learn.microsoft.com/rest/api/fabric/articles/item-management/definitions/semantic-model-definition
- Power BI relationship guidance: https://learn.microsoft.com/power-bi/transform-model/desktop-create-and-manage-relationships
