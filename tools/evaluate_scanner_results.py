#!/usr/bin/env python3
"""Compare normalized scanner findings with an expected anti-pattern manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def _canonical(value: Any) -> str:
    return " ".join(str(value or "").split())


def _key(finding: dict[str, Any]) -> tuple[str, str]:
    return _canonical(finding.get("id")), _canonical(finding.get("object"))


def evaluate(expected_manifest: dict[str, Any], actual_payload: dict[str, Any]) -> dict[str, Any]:
    expected = expected_manifest.get("expected_findings") or []
    actual = actual_payload.get("findings") or []

    expected_map = {_key(item): item for item in expected}
    matched: set[tuple[str, str]] = set()
    false_positive_items: list[dict[str, Any]] = []
    severity_mismatches: list[dict[str, str]] = []

    for item in actual:
        key = _key(item)
        if key in expected_map and key not in matched:
            matched.add(key)
            expected_severity = _canonical(expected_map[key].get("severity"))
            actual_severity = _canonical(item.get("severity"))
            if expected_severity != actual_severity:
                severity_mismatches.append(
                    {
                        "id": key[0],
                        "object": key[1],
                        "expected": expected_severity,
                        "actual": actual_severity,
                    }
                )
        else:
            false_positive_items.append(item)

    false_negative_items = [
        item for key, item in expected_map.items() if key not in matched
    ]

    clean_objects = {
        _canonical(item.get("object"))
        for item in (expected_manifest.get("clean_controls") or [])
        if _canonical(item.get("object"))
    }
    clean_control_violations = [
        item for item in actual if _canonical(item.get("object")) in clean_objects
    ]

    tp = len(matched)
    fp = len(false_positive_items)
    fn = len(false_negative_items)

    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "severity_mismatches": severity_mismatches,
        "clean_control_violations": clean_control_violations,
        "false_positive_items": false_positive_items,
        "false_negative_items": false_negative_items,
    }


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected_manifest", type=Path)
    parser.add_argument("actual_results", type=Path)
    args = parser.parse_args()

    result = evaluate(_load_yaml(args.expected_manifest), _load_json(args.actual_results))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
