# Bad Model Scenarios

These scenarios are ready-made recipes for creating intentionally poor Power BI semantic models.

---

## Scenario A — Retail Mega Model

**Goal:** test basic schema, storage, naming, date, and relationship rules.

### Clean baseline

```text
DimDate -----------+
DimCustomer -------+--> FactSales <-- DimProduct
DimStore ----------+
```

### Inject these anti-patterns

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

### Implementation recipe

- Flatten CustomerName, CustomerSegment, ProductName, ProductCategory, StoreCity, StoreRegion into `FactSales`.
- Repeat order-header freight or discount totals across order-line rows.
- Set Customer → Sales and Product → Sales relationships to Both where relationships remain.
- Do not create a dedicated marked Date table; use `FactSales[OrderDate]` directly.
- Keep `TransactionGUID`, `Comment`, and `ReceiptURL` in the large fact table.
- Keep numeric source key `ProductKey` as text in one table.
- Create `LineValue = FactSales[Quantity] * FactSales[UnitPrice]` as a calculated column.
- Leave raw Amount/Quantity columns visible and rely on implicit Sum.
- Name objects `Sales_Final_v2`, `TEMP_Customer`, `DimProductCopy`, and `Measure 7`.
- Leave keys visible and descriptions empty.

### Intentionally clean controls

- One explicit measure `Net Sales` with correct currency format.
- `DimStore` uses a clean business name and single-direction relationship.
- One low-cardinality integer key is correctly typed and hidden.

---

## Scenario B — Relationship Maze

**Goal:** stress graph analysis and filter-propagation rules.

### Starting tables

```text
DimDate
DimCustomer
DimProduct
FactSales
FactReturns
FactTargets
CustomerProductBridge
```

### Inject these anti-patterns

```text
AP-REL-001
AP-REL-002
AP-REL-003
AP-REL-004
AP-REL-005
AP-REL-006
AP-SCH-005
AP-DATE-003
```

### Implementation recipe

- Create direct `FactSales` ↔ `FactReturns` relationship on OrderNumber.
- Configure multiple dimension relationships as bidirectional.
- Create a direct many-to-many relationship between Customer and Product rather than using the bridge correctly.
- Split a simple customer profile into `CustomerBase` and `CustomerExtra` with an unnecessary 1:1 relationship.
- Duplicate `DimCustomer` as `DimCustomerCopy` for `FactReturns`.
- Create a relationship using customer email or product description text.
- Connect Date to OrderDate actively and ShipDate/DueDate inactively but provide no role-specific measures.
- Ensure at least one ambiguous active filter path exists.

### Intentionally clean controls

- One fact uses a conventional single-direction star relationship.
- One inactive relationship is justified and accompanied by a correct `USERELATIONSHIP` measure.

---

## Scenario C — Bloated Import Model

**Goal:** test size, cardinality, and unnecessary-object detection.

### Inject these anti-patterns

```text
AP-COL-001
AP-COL-002
AP-COL-003
AP-COL-004
AP-COL-005
AP-CALC-001
AP-CALC-002
AP-CALC-004
AP-CALC-005
AP-DATE-002
```

### Implementation recipe

- Import every source column from the transaction system.
- Include unique GUID, URL, notes, source filename, load timestamp, and audit payload.
- Store integer IDs as text.
- Preserve excessive decimal precision.
- Duplicate Year/Month/Quarter labels across each large fact table.
- Add multiple calculated columns that could have been created upstream.
- Add a calculated summary table that duplicates data already available through measures.
- Create several equivalent `Total Sales` measures with different names.
- Add iterator-heavy measures over the entire fact table.
- Keep Auto date/time behavior with many date columns.

### Intentionally clean controls

- A compact integer foreign key.
- A simple `SUM(FactSales[SalesAmount])` measure.
- One dimension with only analytically required columns.

---

## Scenario D — Governance and AI-Unfriendly Model

**Goal:** test semantic quality, metadata, naming, and maintainability rules.

### Inject these anti-patterns

```text
AP-META-001
AP-META-002
AP-META-003
AP-META-004
AP-META-005
AP-CALC-003
AP-CALC-004
AP-SCH-005
```

### Implementation recipe

- Use `Table1`, `Query2`, `STG_SALES_FINAL2`, `TEMP_CUSTOMER`, and `DimCustomerCopy`.
- Use `col1`, `amt`, `v1`, `desc2`, and `Measure 7`.
- Expose surrogate keys and technical audit fields.
- Leave descriptions blank.
- Scatter measures among several tables and leave display folders blank.
- Leave percentages and currencies with General formatting.
- Duplicate semantically equivalent measures.
- Duplicate a dimension and give each copy slightly different names/metadata.

### Intentionally clean controls

- A small number of clearly named and documented measures.
- One well-described dimension that the scanner should not flag.

---

## Scenario E — Mixed Benchmark Model

**Goal:** create a realistic benchmark with both good and bad design for precision/recall measurement.

### Recommended composition

```text
Tables:         10–15
Relationships:  12–20
Measures:       25–40
Calculated cols: 5–10
Expected issues: 20–30
Clean controls:  8–12
```

Select anti-patterns across at least six families. Do not make every table problematic.

Suggested manifest:

```yaml
expected_findings:
  - AP-SCH-001
  - AP-SCH-003
  - AP-REL-001
  - AP-REL-003
  - AP-REL-005
  - AP-DATE-001
  - AP-DATE-003
  - AP-COL-001
  - AP-COL-002
  - AP-COL-003
  - AP-COL-005
  - AP-CALC-001
  - AP-CALC-003
  - AP-CALC-004
  - AP-CALC-005
  - AP-META-001
  - AP-META-002
  - AP-META-003
  - AP-META-004
  - AP-META-005
```

The model should remain sufficiently functional to support metadata scanning, DAX execution, refresh testing, and report creation.
