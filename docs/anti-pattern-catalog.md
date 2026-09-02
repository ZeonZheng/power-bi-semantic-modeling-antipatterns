# Semantic Modeling Anti-Pattern Catalog

This catalog defines intentionally bad Power BI semantic-model designs for negative testing.

Each entry contains:
- **ID**: stable identifier for automation.
- **Severity**: suggested scanner severity.
- **Bad design**: what to deliberately build.
- **Why it is bad**: expected production impact.
- **Detection hints**: metadata or behavioral signals.
- **Production remediation**: what a real model should do instead.

---

## 1. Schema and Grain

### AP-SCH-001 — Flat Mega Table
**Severity:** Warning

**Bad design**
- Put transaction facts, customer attributes, product attributes, geography, and date descriptions into one very wide imported table.
- Duplicate dimension attributes across many fact rows.

**Why it is bad**
- Increases model size through repeated values.
- Hides dimensional structure and business grain.
- Makes reuse, filtering, and governance harder.

**Detection hints**
- Very wide fact-like table.
- Many descriptive text columns on a high-row-count table.
- Few or no dimension tables despite multiple descriptive attribute groups.

**Production remediation**
- Split into a star schema with fact and dimension tables.

### AP-SCH-002 — Mixed Table Responsibility
**Severity:** Warning

**Bad design**
- Store both dimension-like master data and event/transaction rows in the same table.
- Mix slowly changing attributes with additive measures.

**Why it is bad**
- Makes table grain unclear.
- Produces confusing relationship and aggregation behavior.

**Detection hints**
- Table contains identifiers, descriptive attributes, transaction dates, quantities, and amounts together.

**Production remediation**
- Define a single business grain per table and separate facts from dimensions.

### AP-SCH-003 — Inconsistent Fact Grain
**Severity:** Error

**Bad design**
- Mix order-header totals and order-line values in the same fact table.
- Repeat header-level amounts on each detail row.

**Why it is bad**
- Causes double counting and ambiguous aggregation semantics.

**Detection hints**
- Measures aggregate a column that repeats at a lower grain.
- Multiple natural keys imply different grains in one table.

**Production remediation**
- Separate fact tables by grain or allocate values explicitly.

### AP-SCH-004 — Excessive Snowflake for Simple Dimensions
**Severity:** Info

**Bad design**
- Split simple descriptive hierarchies such as Product → Subcategory → Category into several dimension tables even when denormalization is practical.

**Why it is bad**
- Adds relationship complexity and user navigation friction.

**Detection hints**
- Chains of small 1:* dimension tables.
- Multiple dimension-to-dimension relationships for basic attributes.

**Production remediation**
- Prefer a denormalized dimension where appropriate.

### AP-SCH-005 — Duplicate Dimensions Instead of Conformed Dimensions
**Severity:** Warning

**Bad design**
- Create multiple near-identical Customer or Product dimension tables for different fact tables.

**Why it is bad**
- Produces inconsistent filtering and duplicate metadata.

**Detection hints**
- Multiple dimension tables with highly overlapping columns and values.

**Production remediation**
- Reuse conformed dimensions where business semantics are shared.

---

## 2. Relationships

### AP-REL-001 — Unnecessary Bidirectional Filtering
**Severity:** Error

**Bad design**
- Configure dimension-to-fact relationships with cross-filter direction = Both without a specific requirement.

**Why it is bad**
- Can create ambiguous propagation paths and difficult-to-debug filter behavior.

**Detection hints**
- Many relationships use bidirectional cross-filtering.

**Production remediation**
- Default to single-direction filtering from dimension to fact.

### AP-REL-002 — Many-to-Many Shortcut
**Severity:** Error

**Bad design**
- Connect two tables directly with many-to-many cardinality when a bridge dimension should model the relationship.

**Why it is bad**
- Can produce confusing totals and filter behavior.

**Detection hints**
- M:M relationship between business entities or fact-like tables.

**Production remediation**
- Introduce an appropriate bridge table and explicit model semantics.

### AP-REL-003 — Fact-to-Fact Relationship
**Severity:** Error

**Bad design**
- Relate two transaction/fact tables directly on a business key.

**Why it is bad**
- Makes filter propagation and grain interaction difficult to reason about.

**Detection hints**
- Relationship endpoints both have high row counts and additive numeric columns.

**Production remediation**
- Connect facts through shared dimensions.

### AP-REL-004 — One-to-One Relationship Misuse
**Severity:** Warning

**Bad design**
- Split a logically single entity into two tables and connect them 1:1 without a security, storage, or lifecycle reason.

**Why it is bad**
- Adds unnecessary complexity and can obscure the model.

**Detection hints**
- 1:1 relationships between tables with matching row counts and tightly overlapping business keys.

**Production remediation**
- Merge the attributes into one dimension when practical.

### AP-REL-005 — Ambiguous Relationship Paths
**Severity:** Error

**Bad design**
- Build multiple active routes between dimensions and facts, often using bidirectional relationships.

**Why it is bad**
- Filters can propagate through more than one path, producing ambiguous or unintended results.

**Detection hints**
- Graph analysis finds multiple active paths between the same logical entities.

**Production remediation**
- Redesign relationship topology and keep only the required filter path active.

### AP-REL-006 — Relationship on Descriptive Text
**Severity:** Warning

**Bad design**
- Join tables on customer name, product description, or other mutable text rather than stable keys.

**Why it is bad**
- Text keys consume more memory and are vulnerable to duplicates/data-quality changes.

**Detection hints**
- Relationship columns are long text strings rather than compact surrogate/business keys.

**Production remediation**
- Use stable, compact keys.

---

## 3. Date and Time Modeling

### AP-DATE-001 — No Proper Date Dimension
**Severity:** Error

**Bad design**
- Use transaction date columns directly from fact tables for all date slicing.
- Do not create or mark a dedicated date table.

**Why it is bad**
- Reduces consistency and complicates reusable time intelligence.

**Detection hints**
- Multiple date columns exist but no dedicated/marked date dimension is present.

**Production remediation**
- Create a contiguous date dimension and mark it appropriately.

### AP-DATE-002 — Multiple Auto Date/Time Tables
**Severity:** Warning

**Bad design**
- Leave Auto date/time enabled in a model containing many date columns.

**Why it is bad**
- Creates hidden local date tables and increases model metadata/storage overhead.

**Detection hints**
- Hidden local date tables for numerous date columns.

**Production remediation**
- Use a shared date dimension for managed enterprise models.

### AP-DATE-003 — Poor Role-Playing Date Design
**Severity:** Warning

**Bad design**
- Use one Date table with several inactive relationships but provide no clear measures, naming, or UX for Order Date vs Ship Date vs Due Date.

**Why it is bad**
- Creates confusing analytical semantics.

**Detection hints**
- Multiple inactive relationships from a date table to one fact with no associated USERELATIONSHIP measures or role-specific naming.

**Production remediation**
- Deliberately design role-playing date semantics using active/inactive relationships or duplicated role dimensions as appropriate.

---

## 4. Columns, Data Types, and Storage

### AP-COL-001 — High-Cardinality Text in Large Fact Table
**Severity:** Warning

**Bad design**
- Import GUIDs, comments, URLs, long descriptions, or concatenated IDs for every transaction row.

**Why it is bad**
- High-cardinality text compresses poorly and can materially increase VertiPaq size.

**Detection hints**
- Text column cardinality approaches row count on a large table.

**Production remediation**
- Remove unused columns, replace with compact keys, or keep detail outside the semantic model when possible.

### AP-COL-002 — Unused Imported Columns
**Severity:** Warning

**Bad design**
- Load source-system audit fields, ETL metadata, free-text notes, timestamps, and unused IDs that are never used in relationships, measures, sorting, security, or report visuals.

**Why it is bad**
- Consumes memory and refresh resources for no analytical value.

**Detection hints**
- Imported columns have no dependency/reference and are not hidden system keys needed for relationships.

**Production remediation**
- Remove unnecessary columns as early as practical.

### AP-COL-003 — Wrong Data Type
**Severity:** Warning

**Bad design**
- Store numeric keys as text.
- Store dates as text.
- Use decimal/floating types where whole numbers are sufficient.

**Why it is bad**
- Can hurt compression, correctness, sorting, and DAX behavior.

**Detection hints**
- Numeric-looking strings, date-like strings, or unnecessarily wide numeric types.

**Production remediation**
- Use the narrowest semantically correct data type.

### AP-COL-004 — Excessive Precision
**Severity:** Info

**Bad design**
- Keep highly precise decimal values where business requirements only need a small number of decimal places.

**Why it is bad**
- Can reduce compression efficiency and increase storage.

**Detection hints**
- Decimal columns contain more precision than reporting requirements need.

**Production remediation**
- Round/transform at ingestion when acceptable.

### AP-COL-005 — Redundant Derived Columns
**Severity:** Warning

**Bad design**
- Store Year, MonthName, YearMonthText, QuarterText, concatenated labels, and duplicated business logic across large fact tables.

**Why it is bad**
- Duplicates derivable data and metadata.

**Detection hints**
- Numerous derived descriptive columns in fact tables.

**Production remediation**
- Centralize reusable attributes in dimensions and avoid redundant storage.

---

## 5. Calculations and Measures

### AP-CALC-001 — Avoidable Calculated Column on Large Fact
**Severity:** Warning

**Bad design**
- Create calculated columns for values that can be computed upstream or represented as measures.

**Why it is bad**
- Calculated columns are materialized and increase model size.

**Detection hints**
- Large fact table contains calculated columns with row-by-row arithmetic or categorization.

**Production remediation**
- Prefer source/Power Query transformations for static values and measures for dynamic aggregations.

### AP-CALC-002 — Unnecessary Calculated Table
**Severity:** Warning

**Bad design**
- Materialize duplicate or summary tables with DAX even when the same requirement can be modeled cleanly in the source/model.

**Why it is bad**
- Adds processing/storage and dependency complexity.

**Detection hints**
- Calculated tables duplicate imported data or simple groupings.

**Production remediation**
- Use the appropriate ingestion/modeling layer.

### AP-CALC-003 — Implicit Measures Everywhere
**Severity:** Warning

**Bad design**
- Expose raw numeric fact columns and rely on drag-and-drop implicit Sum/Average rather than governed explicit measures.

**Why it is bad**
- Business logic becomes inconsistent and harder to govern.

**Detection hints**
- Many visible numeric fact columns and few explicit measures.

**Production remediation**
- Create explicit, documented measures for governed analytics.

### AP-CALC-004 — Duplicate Measures
**Severity:** Warning

**Bad design**
- Create several measures with identical or nearly identical expressions under different names.

**Why it is bad**
- Increases semantic clutter and maintenance cost.

**Detection hints**
- Normalized DAX expressions are identical or trivially equivalent.

**Production remediation**
- Reuse a canonical measure and reference it from derived measures.

### AP-CALC-005 — Expensive Iterator Over Entire Fact Table
**Severity:** Warning

**Bad design**
- Use SUMX/FILTER patterns over a very large fact table when a simpler native aggregation or better model design would suffice.

**Why it is bad**
- Can increase formula-engine work and query latency.

**Detection hints**
- Measures iterate entire high-row-count tables without selective filters or necessity.

**Production remediation**
- Simplify DAX and optimize model shape before relying on expensive iteration.

---

## 6. Naming, Metadata, and Usability

### AP-META-001 — Technical/Temporary Object Names
**Severity:** Warning

**Bad design**
- Use names such as `Table1`, `Query2`, `STG_SALES_FINAL2`, `TEMP_CUSTOMER`, `DimCustomerCopy`, `col1`, or `Measure 7`.

**Why it is bad**
- Lowers maintainability, discoverability, and AI interpretability.

**Detection hints**
- Prefixes/patterns such as STG_, TEMP_, Copy, TableN, QueryN, generic column names.

**Production remediation**
- Use stable business-oriented names.

### AP-META-002 — Exposed Technical Keys
**Severity:** Info

**Bad design**
- Leave surrogate keys, source IDs, and relationship-only technical fields visible to report authors.

**Why it is bad**
- Clutters the field list and encourages incorrect usage.

**Detection hints**
- Visible columns participate only in relationships and have names ending in Key/ID/SK.

**Production remediation**
- Hide technical fields not intended for reporting.

### AP-META-003 — Missing Descriptions
**Severity:** Info

**Bad design**
- Leave tables, measures, and important columns undocumented.

**Why it is bad**
- Reduces usability for developers, self-service users, and AI agents.

**Detection hints**
- Description metadata is blank across most semantic objects.

**Production remediation**
- Document business meaning, calculation intent, and edge cases.

### AP-META-004 — Poor Measure Organization
**Severity:** Info

**Bad design**
- Scatter measures across random fact tables with no display folders or consistent naming.

**Why it is bad**
- Makes the model difficult to navigate and govern.

**Detection hints**
- Large number of measures with blank display folders and inconsistent table placement.

**Production remediation**
- Apply a consistent measure organization strategy.

### AP-META-005 — Inconsistent Formatting
**Severity:** Info

**Bad design**
- Leave currency as General, percentages as decimals, dates with inconsistent formats, or use inconsistent decimal precision across related measures.

**Why it is bad**
- Produces confusing report behavior and poor semantic quality.

**Detection hints**
- Business measures have default/blank or obviously inconsistent format strings.

**Production remediation**
- Apply intentional semantic formatting.

---

## 7. Security and Model Behavior

### AP-SEC-001 — RLS Embedded in Ad-Hoc Business Logic
**Severity:** Warning

**Bad design**
- Spread complex user-access conditions across unrelated tables and DAX expressions rather than modeling security deliberately.

**Why it is bad**
- Hard to validate, maintain, and reason about.

**Detection hints**
- Multiple complex RLS filters reference many unrelated tables/functions.

**Production remediation**
- Use a clear security mapping design and validate relationship propagation.

### AP-SEC-002 — RLS on Fact Table When Dimension Security Is Sufficient
**Severity:** Warning

**Bad design**
- Apply row-level security directly to a large fact table when users can be filtered through a smaller dimension.

**Why it is bad**
- Can add complexity and reduce clarity/performance.

**Detection hints**
- RLS expressions are defined on high-row-count fact tables and equivalent dimension filtering is available.

**Production remediation**
- Prefer dimension-based security where the business model allows it.

---

## Suggested Test Coverage

A balanced deliberately poor model should normally contain defects from several independent families rather than twenty variants of the same issue.

Recommended minimum test pack:

```text
Schema       3 anti-patterns
Relationship 4 anti-patterns
Date         2 anti-patterns
Storage      4 anti-patterns
Calculation  3 anti-patterns
Metadata     4 anti-patterns
Security     1 anti-pattern
---------------------------
Total       21 expected findings
```

For scanner validation, store the selected anti-pattern IDs as the model's expected finding manifest and compare them with actual scanner output.
