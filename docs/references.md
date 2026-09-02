# References

This repository intentionally describes bad modeling practices by inverting established Power BI / tabular modeling guidance. The links below are the primary references to consult when validating or extending the anti-pattern catalog.

## Microsoft Learn — Semantic model design

### Star schema guidance
https://learn.microsoft.com/power-bi/guidance/star-schema

Used to support anti-patterns involving:
- flat mega tables;
- mixed fact/dimension responsibilities;
- inconsistent fact grain;
- duplicate/non-conformed dimensions;
- excessive snowflaking where a denormalized dimension is more appropriate.

### Model relationships guidance
https://learn.microsoft.com/power-bi/guidance/relationships-bidirectional-filtering

Used to support anti-patterns involving:
- unnecessary bidirectional relationships;
- complex/ambiguous filtering behavior.

### Many-to-many relationship guidance
https://learn.microsoft.com/power-bi/guidance/relationships-many-to-many

Used to support anti-patterns involving:
- direct many-to-many shortcuts;
- bridge-table modeling choices;
- fact-to-fact style relationship problems.

### Active vs inactive relationship guidance
https://learn.microsoft.com/power-bi/guidance/relationships-active-inactive

Used to support anti-patterns involving:
- poorly designed role-playing dimensions;
- unclear Order Date / Ship Date / Due Date semantics.

### Date table guidance
https://learn.microsoft.com/power-bi/guidance/model-date-tables

Used to support anti-patterns involving:
- missing dedicated date dimensions;
- unsuitable date-table design.

### Auto date/time guidance
https://learn.microsoft.com/power-bi/transform-model/desktop-auto-date-time

Used to support anti-patterns involving:
- hidden local date-table proliferation in managed enterprise models.

## Microsoft Learn — Model size and optimization

### Data reduction techniques for Import modeling
https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction

Used to support anti-patterns involving:
- unused imported columns;
- excessive rows/detail;
- high-cardinality data;
- unnecessary precision;
- avoidable model bloat.

### Use calculated columns guidance
https://learn.microsoft.com/power-bi/transform-model/desktop-calculated-columns

Provides context for calculated-column behavior. The catalog treats calculated columns as anti-patterns only when they are unnecessary, duplicated, or materially worsen large-model storage/maintenance.

### Measures guidance
https://learn.microsoft.com/power-bi/transform-model/desktop-measures

Used as background for explicit measure design and reusable calculation semantics.

## Tabular Editor — Best Practice Analyzer

### Best Practice Analyzer documentation
https://docs.tabulareditor.com/te2/Best-Practice-Analyzer.html

### Community Best Practice Rules repository
https://github.com/TabularEditor/BestPracticeRules

These are useful references when translating modeling guidance into machine-detectable metadata rules. They are especially relevant to:
- naming and descriptions;
- visible keys;
- measure organization;
- relationship settings;
- object-level metadata checks;
- DAX/model maintainability.

## Microsoft semantic model / TMDL documentation

### Tabular Model Definition Language (TMDL)
https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview

Useful when an AI agent needs to generate or intentionally modify semantic-model metadata as source-controlled text.

## Important interpretation note

Not every guideline is an absolute rule. Modeling decisions can be context-dependent. For example:
- bidirectional filtering can be justified in specific scenarios;
- many-to-many relationships can be legitimate;
- calculated columns can be appropriate;
- snowflake dimensions can be necessary;
- duplicated role-playing dimensions can improve usability.

Therefore this repository uses phrases such as **unnecessary**, **avoidable**, **misuse**, or **without a specific requirement**. Scanner implementations should combine metadata rules with model context rather than treating every occurrence as inherently defective.

## Recommended extension process

When adding a new anti-pattern:

1. Link it to authoritative guidance or a well-established BPA rule.
2. Define the context in which the pattern is genuinely undesirable.
3. Add a stable ID.
4. Provide deterministic detection hints.
5. Add at least one bad example and, where useful, one clean counterexample.
6. Update `rules/antipatterns.yaml` so AI/tooling can consume it.
