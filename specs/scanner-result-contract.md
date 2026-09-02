# Scanner Result Contract

The evaluator consumes normalized scanner output independent of the scanner's native schema.

## Input JSON

```json
{
  "findings": [
    {
      "id": "AP-REL-001",
      "object": "TEMP_Customer -> Sales_Final_v2",
      "severity": "Error"
    }
  ]
}
```

Required per finding:

- `id`: anti-pattern ID such as `AP-REL-001`;
- `object`: canonical target object string used by the expected manifest;
- `severity`: `Info`, `Warning`, or `Error`.

Extra fields are allowed and are preserved when a finding is reported as a false positive or clean-control violation.

## Matching

A finding matches ground truth when `(id, object)` matches after whitespace normalization. Severity is intentionally not part of the identity key. If ID and object match but severity differs, the item counts as detected and is also emitted in `severity_mismatches`.

Duplicate actual findings for the same `(id, object)` are not double-counted as true positives; the additional copies are false positives.

## Clean controls

Any actual finding targeting an object listed under `clean_controls` in the expected manifest is reported in `clean_control_violations`. This is independent of TP/FP accounting and highlights likely false positives on deliberately clean objects.

## Metric conventions

- `precision = TP / (TP + FP)`; if no findings are produced, precision is `1.0`.
- `recall = TP / (TP + FN)`; if no findings are expected, recall is `1.0`.
- `F1` is the harmonic mean of precision and recall.
- When both expected and actual finding sets are empty, precision, recall, and F1 are all `1.0`.

## CLI

```bash
python tools/evaluate_scanner_results.py \
  manifests/bad-basic.expected.yaml \
  actual-findings.json
```

The command prints a JSON report containing TP/FP/FN, precision, recall, F1, mismatches, and detailed unmatched items.
