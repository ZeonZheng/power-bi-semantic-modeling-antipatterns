#!/usr/bin/env python3
"""Validate anti-pattern test-kit contracts without Power BI/Fabric dependencies."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

V1_IDS = {
    'AP-SCH-001','AP-SCH-003','AP-REL-001','AP-DATE-001','AP-COL-001','AP-COL-002','AP-COL-003',
    'AP-CALC-001','AP-CALC-003','AP-META-001','AP-META-002','AP-META-003','AP-META-005'
}
EXECUTABLE_FIELDS = ('implementation', 'expected_detection', 'verification')


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open('r', encoding='utf-8') as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError:
        return {}
    return data if isinstance(data, dict) else {}


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_controls(items: Any, source: str, errors: list[str]) -> None:
    if items is None:
        return
    if not isinstance(items, list):
        errors.append(f'{source}: clean_controls must be a list')
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f'{source}: clean control #{index + 1} must be an object')
            continue
        if not (_non_empty(item.get('object')) and _non_empty(item.get('object_type')) and isinstance(item.get('expectations'), dict) and item.get('expectations')):
            errors.append(f'{source}: clean control must contain object, object_type, and non-empty expectations')


def validate_repository(root: Path) -> list[str]:
    root = Path(root)
    errors: list[str] = []

    rules_doc = _load_yaml(root / 'rules/antipatterns.yaml')
    rules = rules_doc.get('antipatterns') or []
    if not isinstance(rules, list):
        return ['rules/antipatterns.yaml: antipatterns must be a list']

    ids = [item.get('id') for item in rules if isinstance(item, dict) and _non_empty(item.get('id'))]
    counts = Counter(ids)
    for rule_id, count in counts.items():
        if count > 1:
            errors.append(f'rules/antipatterns.yaml: duplicate anti-pattern ID {rule_id}')

    rule_map = {item.get('id'): item for item in rules if isinstance(item, dict) and _non_empty(item.get('id'))}
    for rule_id in sorted(V1_IDS):
        rule = rule_map.get(rule_id)
        if rule is None:
            errors.append(f'rules/antipatterns.yaml: missing V1 anti-pattern ID {rule_id}')
            continue
        for field in EXECUTABLE_FIELDS:
            if not isinstance(rule.get(field), dict) or not rule.get(field):
                errors.append(f'rules/antipatterns.yaml: {rule_id} missing executable field {field}')

    expected_doc = _load_yaml(root / 'manifests/bad-basic.expected.yaml')
    expected_findings = expected_doc.get('expected_findings') or []
    if not isinstance(expected_findings, list):
        errors.append('manifests/bad-basic.expected.yaml: expected_findings must be a list')
        expected_findings = []
    expected_ids: set[str] = set()
    for index, item in enumerate(expected_findings):
        if not isinstance(item, dict):
            errors.append(f'manifests/bad-basic.expected.yaml: expected finding #{index + 1} must be an object')
            continue
        rule_id = item.get('id')
        if rule_id not in rule_map:
            errors.append(f'manifests/bad-basic.expected.yaml: unknown anti-pattern ID {rule_id}')
        elif isinstance(rule_id, str):
            expected_ids.add(rule_id)
        if not _non_empty(item.get('object')):
            errors.append('manifests/bad-basic.expected.yaml: expected finding object must be non-empty')
        if not _non_empty(item.get('severity')):
            errors.append('manifests/bad-basic.expected.yaml: expected finding severity must be non-empty')

    missing_expected = sorted(V1_IDS - expected_ids)
    if missing_expected:
        errors.append('manifests/bad-basic.expected.yaml: missing V1 expected IDs ' + ', '.join(missing_expected))

    _validate_controls(expected_doc.get('clean_controls'), 'manifests/bad-basic.expected.yaml', errors)

    baseline_controls = _load_yaml(root / 'manifests/baseline-clean.controls.yaml')
    _validate_controls(baseline_controls.get('clean_controls'), 'manifests/baseline-clean.controls.yaml', errors)

    model_doc = _load_yaml(root / 'models/bad-basic/model-manifest.yaml')
    mutations = model_doc.get('mutations') or []
    if not isinstance(mutations, list):
        errors.append('models/bad-basic/model-manifest.yaml: mutations must be a list')
        mutations = []
    mutation_ids: set[str] = set()
    for index, item in enumerate(mutations):
        if not isinstance(item, dict):
            errors.append(f'models/bad-basic/model-manifest.yaml: mutation #{index + 1} must be an object')
            continue
        rule_id = item.get('id')
        if rule_id not in rule_map:
            errors.append(f'models/bad-basic/model-manifest.yaml: unknown anti-pattern ID {rule_id}')
        elif isinstance(rule_id, str):
            mutation_ids.add(rule_id)
        targets = item.get('targets')
        if not isinstance(targets, list) or not targets or not all(_non_empty(x) for x in targets):
            errors.append(f'models/bad-basic/model-manifest.yaml: mutation {rule_id} must contain non-empty targets')
        if not _non_empty(item.get('change')):
            errors.append(f'models/bad-basic/model-manifest.yaml: mutation {rule_id} must contain a non-empty change')

    missing_mutations = sorted(V1_IDS - mutation_ids)
    if missing_mutations:
        errors.append('models/bad-basic/model-manifest.yaml: missing V1 mutations ' + ', '.join(missing_mutations))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.', type=Path)
    args = parser.parse_args()

    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        print(f'Validation failed with {len(errors)} error(s).')
        return 1
    print('Contract validation passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
