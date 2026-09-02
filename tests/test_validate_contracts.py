from pathlib import Path
import yaml

from tools.validate_contracts import validate_repository

V1_IDS = [
    'AP-SCH-001','AP-SCH-003','AP-REL-001','AP-DATE-001','AP-COL-001','AP-COL-002','AP-COL-003',
    'AP-CALC-001','AP-CALC-003','AP-META-001','AP-META-002','AP-META-003','AP-META-005'
]


def write_yaml(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding='utf-8')


def executable_rule(rule_id):
    return {
        'id': rule_id,
        'family': 'test',
        'name': rule_id,
        'severity': 'Warning',
        'inject': 'inject',
        'detect': ['detect'],
        'remediate': 'fix',
        'implementation': {
            'target_type': 'column',
            'preconditions': ['exists'],
            'baseline': {'state': 'clean'},
            'mutation': {'state': 'bad'},
        },
        'expected_detection': {'object_type': 'column', 'evidence': {'state': 'bad'}},
        'verification': {'method': 'metadata', 'deterministic': True},
    }


def make_valid_repo(root: Path):
    write_yaml(root/'rules/antipatterns.yaml', {'antipatterns': [executable_rule(x) for x in V1_IDS]})
    write_yaml(root/'models/bad-basic/model-manifest.yaml', {
        'mutations': [{'id': x, 'targets': [f'Object{x}'], 'change': 'bad'} for x in V1_IDS]
    })
    write_yaml(root/'manifests/bad-basic.expected.yaml', {
        'expected_findings': [{'id': x, 'object': f'Object{x}', 'severity': 'Warning'} for x in V1_IDS],
        'clean_controls': [{'object': 'Clean[Key]', 'object_type': 'column', 'expectations': {'hidden': True}}],
    })
    write_yaml(root/'manifests/baseline-clean.controls.yaml', {
        'clean_controls': [{'object': 'Clean[Key]', 'object_type': 'column', 'expectations': {'hidden': True}}]
    })


def test_valid_contracts_pass(tmp_path):
    make_valid_repo(tmp_path)
    assert validate_repository(tmp_path) == []


def test_unknown_antipattern_id_fails(tmp_path):
    make_valid_repo(tmp_path)
    manifest = yaml.safe_load((tmp_path/'manifests/bad-basic.expected.yaml').read_text())
    manifest['expected_findings'].append({'id': 'AP-UNKNOWN-999', 'object': 'X', 'severity': 'Warning'})
    write_yaml(tmp_path/'manifests/bad-basic.expected.yaml', manifest)
    errors = validate_repository(tmp_path)
    assert any('unknown anti-pattern ID AP-UNKNOWN-999' in x for x in errors)


def test_duplicate_rule_id_fails(tmp_path):
    make_valid_repo(tmp_path)
    rules = yaml.safe_load((tmp_path/'rules/antipatterns.yaml').read_text())
    rules['antipatterns'].append(executable_rule(V1_IDS[0]))
    write_yaml(tmp_path/'rules/antipatterns.yaml', rules)
    errors = validate_repository(tmp_path)
    assert any(f'duplicate anti-pattern ID {V1_IDS[0]}' in x for x in errors)


def test_missing_executable_fields_for_v1_rule_fails(tmp_path):
    make_valid_repo(tmp_path)
    rules = yaml.safe_load((tmp_path/'rules/antipatterns.yaml').read_text())
    del rules['antipatterns'][0]['verification']
    write_yaml(tmp_path/'rules/antipatterns.yaml', rules)
    errors = validate_repository(tmp_path)
    assert any(f'{V1_IDS[0]} missing executable field verification' in x for x in errors)


def test_empty_expected_object_fails(tmp_path):
    make_valid_repo(tmp_path)
    manifest = yaml.safe_load((tmp_path/'manifests/bad-basic.expected.yaml').read_text())
    manifest['expected_findings'][0]['object'] = '   '
    write_yaml(tmp_path/'manifests/bad-basic.expected.yaml', manifest)
    errors = validate_repository(tmp_path)
    assert any('expected finding object must be non-empty' in x for x in errors)


def test_malformed_clean_control_fails(tmp_path):
    make_valid_repo(tmp_path)
    controls = yaml.safe_load((tmp_path/'manifests/baseline-clean.controls.yaml').read_text())
    controls['clean_controls'][0].pop('expectations')
    write_yaml(tmp_path/'manifests/baseline-clean.controls.yaml', controls)
    errors = validate_repository(tmp_path)
    assert any('clean control must contain object, object_type, and non-empty expectations' in x for x in errors)
