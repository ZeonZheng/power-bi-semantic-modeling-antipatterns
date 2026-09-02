# Anti-pattern Test Kit V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic V1 Power BI semantic-model anti-pattern test kit with executable rule contracts, baseline/bad-model manifests, contract validation, scanner scoring, and an AI materialization prompt.

**Architecture:** Keep repository artifacts declarative and Power BI/Fabric-independent. Python utilities only validate contracts and compare normalized scanner findings; PBIP/TMDL materialization remains an agent-driven integration layer governed by the contracts.

**Tech Stack:** YAML, JSON Schema, Python 3.10+, PyYAML, pytest, PBIP/TMDL-compatible documentation.

**Spec:** `docs/superpowers/specs/2026-09-02-antipattern-test-kit-v1-design.md`

## Global Constraints

- V1 must cover exactly the 13 anti-pattern IDs listed in the approved design.
- Generated bad models must remain structurally valid; parser corruption is out of scope.
- No Power BI/Fabric credentials or SDKs are required for validation/scoring utilities.
- Ground truth matching uses anti-pattern ID plus canonical object; severity mismatch is reported separately.
- Python feature implementation follows test-driven development.
- Keep large synthetic datasets out of the repository.

---

## File map

| File | Responsibility |
|---|---|
| `rules/antipattern-schema.json` | Machine-readable schema for executable rules |
| `rules/antipatterns.yaml` | Rule catalog with executable metadata for V1 rules |
| `specs/generation-contract.md` | Contract for model-generation agents |
| `specs/tmdl-mutation-spec.md` | Mapping guidance from mutations to PBIP/TMDL semantics |
| `specs/scanner-result-contract.md` | Normalized scanner-output contract |
| `models/baseline-clean/model-manifest.yaml` | Clean Retail model contract |
| `models/bad-basic/model-manifest.yaml` | Declared mutations for the V1 bad model |
| `manifests/baseline-clean.controls.yaml` | Clean controls used for false-positive testing |
| `manifests/bad-basic.expected.yaml` | V1 expected findings ground truth |
| `tools/validate_contracts.py` | Cross-file contract validation |
| `tools/evaluate_scanner_results.py` | TP/FP/FN and quality metric computation |
| `tests/test_validate_contracts.py` | Validator behavior tests |
| `tests/test_evaluate_scanner_results.py` | Evaluator behavior tests |
| `prompts/generate-v1-retail-model.md` | AI prompt for physical PBIP/TMDL materialization |
| `README.md` | V1 workflow entry point |

---

### Task 1: Contract schema and executable V1 rules

**Files:**
- Create: `rules/antipattern-schema.json`
- Modify: `rules/antipatterns.yaml`

**Interfaces:**
- Produces: executable rule entries with `implementation`, `expected_detection`, and `verification` fields.
- Consumed by: `tools/validate_contracts.py`, generation prompt, manifests.

- [ ] Define JSON Schema requiring `id`, `family`, `name`, `severity`, plus executable metadata when `implementation` is present.
- [ ] Extend the 13 V1 rules with deterministic target type, preconditions, baseline state, mutation state, expected detection evidence, and metadata verification.
- [ ] Keep non-V1 catalog rules valid as descriptive-only entries.
- [ ] Validate YAML parses and all 13 required IDs contain executable metadata.
- [ ] Commit as `feat: add executable V1 anti-pattern contracts`.

### Task 2: Baseline and bad-basic declarative model contracts

**Files:**
- Create: `models/baseline-clean/model-manifest.yaml`
- Create: `models/baseline-clean/README.md`
- Create: `models/bad-basic/model-manifest.yaml`
- Create: `models/bad-basic/README.md`
- Create: `manifests/baseline-clean.controls.yaml`
- Create: `manifests/bad-basic.expected.yaml`

**Interfaces:**
- Produces: deterministic object names and canonical object identifiers used by evaluator matching.
- Consumed by: validator, AI generation prompt, scanner-result evaluation.

- [ ] Define the clean star-schema baseline with five tables, 1:* single-direction relationships, explicit `Net Sales`, hidden keys, descriptions, and formatting.
- [ ] Define `bad-basic` as declared mutations from the baseline rather than an unrelated model.
- [ ] Map all 13 V1 anti-patterns to at least one concrete canonical target object.
- [ ] Record clean controls for objects intentionally kept compliant.
- [ ] Ensure every expected finding references a known V1 rule and a non-empty object.
- [ ] Commit as `feat: add V1 baseline and bad-model manifests`.

### Task 3: Scanner result contract and evaluator — TDD

**Files:**
- Create: `specs/scanner-result-contract.md`
- Create: `tests/test_evaluate_scanner_results.py`
- Create: `tools/evaluate_scanner_results.py`

**Interfaces:**
- Produces: `evaluate(expected_manifest: dict, actual_payload: dict) -> dict` and CLI JSON output.
- Input normalized finding: `{id: str, object: str, severity: str}`.

- [ ] Write tests for exact TP/FP/FN matching, metric calculation, severity mismatch, clean-control violation, and empty sets.
- [ ] Run tests before implementation and verify they fail because the evaluator does not exist.
- [ ] Implement minimal normalization/matching and metric calculation.
- [ ] Re-run tests and verify all evaluator tests pass.
- [ ] Document accepted scanner JSON structure and matching semantics.
- [ ] Commit as `feat: add scanner result evaluator`.

### Task 4: Contract validator — TDD

**Files:**
- Create: `specs/generation-contract.md`
- Create: `specs/tmdl-mutation-spec.md`
- Create: `tests/test_validate_contracts.py`
- Create: `tools/validate_contracts.py`

**Interfaces:**
- Produces: `validate_repository(root: Path) -> list[str]`, where an empty list means valid.
- Consumes: rule catalog, baseline controls, expected findings, model manifests.

- [ ] Write tests for valid fixtures, unknown anti-pattern ID, duplicate rule ID, missing executable V1 fields, empty expected object, and malformed clean control.
- [ ] Run tests before implementation and verify expected failures.
- [ ] Implement YAML loading and cross-file structural checks without Power BI/Fabric dependencies.
- [ ] Re-run validator tests and verify all pass.
- [ ] Document generation and TMDL mutation contracts using the same canonical object names/properties as manifests.
- [ ] Commit as `feat: add repository contract validator`.

### Task 5: AI materialization prompt and V1 workflow documentation

**Files:**
- Create: `prompts/generate-v1-retail-model.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: executable rules, model manifests, expected findings, generation/TMDL contracts.
- Produces: instructions for an agent to create PBIP/TMDL-compatible baseline and bad-basic artifacts.

- [ ] Specify deterministic synthetic-data defaults: 100k sales, 10k customers, 1k products, 50 stores.
- [ ] Require `TransactionGUID` expected distinct ratio >= 0.95.
- [ ] Require generation of baseline first and bad-basic strictly via declared mutations.
- [ ] Require syntax/structure validation and preservation of clean controls.
- [ ] Update README with V1 local validation/scoring commands and repository flow.
- [ ] Commit as `docs: add V1 model materialization workflow`.

### Task 6: End-to-end verification

**Files:**
- Verify all files above; no new production feature required unless a defect is found.

**Interfaces:**
- Uses: `pytest`, `tools/validate_contracts.py`, `tools/evaluate_scanner_results.py`.

- [ ] Run `pytest -q` and require all tests to pass.
- [ ] Run `python tools/validate_contracts.py .` and require zero validation errors.
- [ ] Run evaluator against `manifests/bad-basic.expected.yaml` with a representative normalized scanner-result fixture and inspect metrics.
- [ ] Re-read key GitHub files from `main` after commit to verify repository persistence.
- [ ] Record final commit SHAs and remaining V2 integration work.
