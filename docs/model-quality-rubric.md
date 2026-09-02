# Model Quality Rubric for Negative-Test Models

This rubric is intended to grade **how useful an intentionally poor semantic model is as a scanner test fixture**. It is not a production model scorecard.

## Scoring dimensions

| Dimension | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Defect traceability | No manifest | Partial notes | Most issues mapped | All issues mapped to stable IDs | IDs, object evidence, and expected severity all recorded |
| Defect diversity | One issue family | Two families | Three-four families | Five-six families | Broad coverage with independent positive/negative controls |
| Realism | Artificial corruption | Mostly contrived | Plausible developer mistakes | Realistic enterprise mistakes | Closely resembles organic low-quality models |
| Detectability | Mostly subjective | Weak metadata signals | Several deterministic signals | Most defects machine-detectable | Clear metadata/dependency/performance evidence for every defect |
| Model usability | Does not load | Loads unreliably | Loads but core analysis broken | Opens and common queries work | Fully scan-able with enough valid behavior for performance testing |
| False-positive control | Everything is bad | Very few clean objects | Some clean controls | Explicit clean controls | Clean controls deliberately resemble bad objects without violating rules |
| Reproducibility | Random generation | Hard to repeat | Partially repeatable | Reproducible instructions | Script/prompt + manifest recreate the same defect set |

Maximum score: **28**.

## Interpretation

```text
0–9    Poor test fixture
10–16  Useful for basic functional checks
17–22  Good scanner regression fixture
23–28  Strong benchmark-quality negative model
```

## Recommended acceptance criteria

A model intended for scanner validation should normally satisfy all of the following:

- score >= 20;
- at least 5 anti-pattern families represented;
- at least 15 expected findings;
- at least 5 intentionally clean controls;
- zero model-corrupting defects unless corruption detection is the test objective;
- every expected finding has an anti-pattern ID and target object;
- severity is defined before the scanner is run.

## Scanner evaluation metrics

Given:

```text
Expected findings = ground-truth manifest
Actual findings   = scanner output
```

calculate:

```text
True Positive  (TP): expected defect correctly detected
False Positive (FP): scanner flags a defect not present in manifest
False Negative (FN): expected defect scanner misses

Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * Precision * Recall / (Precision + Recall)
```

### Example

```text
Expected: 20
Detected:  19
Correct:   17

TP = 17
FP = 2
FN = 3

Precision = 17 / 19 = 89.5%
Recall    = 17 / 20 = 85.0%
F1        = 87.2%
```

## Severity evaluation

Detection alone is not enough. Compare scanner severity with expected severity.

Suggested matrix:

| Expected | Acceptable scanner output |
|---|---|
| Error | Error, or Warning with documented rationale |
| Warning | Warning; Error only if impact is demonstrably high |
| Info | Info; Warning acceptable if environment-specific |

Track severity accuracy separately from detection precision/recall.

## Regression-test recommendation

Keep several benchmark models rather than one giant bad model:

```text
bad-model-basic        obvious metadata/storage defects
bad-model-relations    graph/cardinality/filter defects
bad-model-performance  cardinality/model-size/DAX defects
bad-model-governance   naming/description/organization defects
mixed-control-model    realistic mixture with clean controls
```

This makes scanner regressions easier to isolate.
