from tools.evaluate_scanner_results import evaluate


def expected_manifest():
    return {
        'expected_findings': [
            {'id': 'AP-REL-001', 'object': 'TEMP_Customer -> Sales_Final_v2', 'severity': 'Error'},
            {'id': 'AP-COL-001', 'object': 'Sales_Final_v2[TransactionGUID]', 'severity': 'Warning'},
        ],
        'clean_controls': [
            {'object': 'DimStore[StoreKey]', 'object_type': 'column', 'expectations': {'hidden': True}}
        ],
    }


def test_evaluate_counts_tp_fp_fn_and_metrics():
    actual = {
        'findings': [
            {'id': 'AP-REL-001', 'object': 'TEMP_Customer -> Sales_Final_v2', 'severity': 'Error'},
            {'id': 'AP-META-001', 'object': 'OtherTable', 'severity': 'Warning'},
        ]
    }
    result = evaluate(expected_manifest(), actual)
    assert result['true_positives'] == 1
    assert result['false_positives'] == 1
    assert result['false_negatives'] == 1
    assert result['precision'] == 0.5
    assert result['recall'] == 0.5
    assert result['f1'] == 0.5


def test_severity_mismatch_is_matched_but_reported():
    actual = {
        'findings': [
            {'id': 'AP-REL-001', 'object': 'TEMP_Customer -> Sales_Final_v2', 'severity': 'Warning'},
            {'id': 'AP-COL-001', 'object': 'Sales_Final_v2[TransactionGUID]', 'severity': 'Warning'},
        ]
    }
    result = evaluate(expected_manifest(), actual)
    assert result['true_positives'] == 2
    assert result['false_positives'] == 0
    assert result['false_negatives'] == 0
    assert result['severity_mismatches'] == [
        {
            'id': 'AP-REL-001',
            'object': 'TEMP_Customer -> Sales_Final_v2',
            'expected': 'Error',
            'actual': 'Warning',
        }
    ]


def test_clean_control_violation_is_reported():
    actual = {
        'findings': [
            {'id': 'AP-META-002', 'object': 'DimStore[StoreKey]', 'severity': 'Info'}
        ]
    }
    result = evaluate(expected_manifest(), actual)
    assert result['clean_control_violations'] == [
        {'id': 'AP-META-002', 'object': 'DimStore[StoreKey]', 'severity': 'Info'}
    ]


def test_empty_expected_and_actual_sets_score_as_perfect_empty_case():
    result = evaluate({'expected_findings': [], 'clean_controls': []}, {'findings': []})
    assert result['true_positives'] == 0
    assert result['false_positives'] == 0
    assert result['false_negatives'] == 0
    assert result['precision'] == 1.0
    assert result['recall'] == 1.0
    assert result['f1'] == 1.0
