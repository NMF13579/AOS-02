# R1 — Target Contract Consolidation

```yaml
stage: R1
status: COMPLETE
baseline:
  branch: rebuild/aos02-reference-driven-v1
  commit: 56a89d8acd04eeb82bb38e48c841ddc81bd0883f
  tree: a502d71a445581512dcaa29e5e450c449ffc9fe3
scope: DOCUMENTED_TARGET_BOUNDARY_ONLY
runtime_code_changed: false
schema_changed: false
canonical_contract_changed: false
execution_authority_granted: false
Git_authority_granted: false
next_required_action: R2_CLEAN_PACKAGE_SKELETON
```

## Purpose

Define the target AOS-02 module boundary before moving any v0 implementation code. This mapping is a design contract for the rebuild; it does not replace current canonical contracts, alter schema v2, or grant any runtime capability.

## Canonical-to-target map

| Existing canonical source | Target domain concept | Target owner | Rule preserved |
|---|---|---|---|
| `status-and-glossary-contract.md` | `Status`, `ControlState`, `ReasonCode` | `domain/control_status.py` | `UNKNOWN`, missing data and `NOT_RUN` never become PASS |
| `risk-profile-contract.md` | `RiskProfile` | `domain/records.py` | Risk selection is not trusted authority |
| `scope-and-change-contract.md` | `ScopeAndChange`, `PortablePath` | `domain/scope.py` | closed portable paths; forbidden precedence; no collision |
| `task-brief-contract.md` | `TaskBrief`, `TaskBindings` | `domain/records.py` | bounded draft, not execution/Git authority |
| `human-decision-record-contract.md` | `DecisionProjection`, `AuthorityAssessment` | `domain/authority.py` | local YAML is structural input, never trusted authority |
| `evidence-report-contract.md` | `EvidenceReport`, `CheckObservation` | `domain/evidence.py` | required checks/bindings are exact; Evidence is not approval |
| `delivery-contract.md` | `PublicationIntent` | `domain/delivery.py` | result/publication records never grant Git or release rights |
| `architecture-decision-record-contract.md` | `ArchitectureDecision` | documentation/ADR boundary | no runtime authority implied |

## Application use cases

| Target use case | Input | Output | Non-goal |
|---|---|---|---|
| `validate_bundle` | strict record bundle | structural + semantic result | human approval |
| `compile_task_draft` | Idea, Risk, Scope | draft Task Brief | execution authorization |
| `preview_execution` | valid task/request/decision | blocked read-only preview | filesystem mutation |
| `assess_result` | Evidence + result decision | structural assessment | Git authority |
| `assess_publication` | Evidence + publication decision | structural assessment | push/merge/release |

These live under `application/` and may depend only on domain ports, not `argparse`, file paths, Git commands, or direct YAML parsing.

## Infrastructure adapters

| Existing v0 asset | Target location | R1 disposition |
|---|---|---|
| `loader.py` | `infrastructure/strict_yaml.py` | preserve behavior; relocate in R2 without semantic change |
| `runtime_schema.py` + `schemas/runtime/*.json` | `infrastructure/schema_registry.py` + existing schema data | preserve v2 compatibility boundary |
| `git_preflight.py` | `infrastructure/git_read.py` | preserve as read-only adapter; no Git write port |
| `runtime_records.py` | split between `domain/records.py` and application mapping | replace gradually after contract tests exist |
| `execution.py`, `execution_preview.py`, `execution_decision.py` | `application/execution_preview.py` | preserve non-mutating boundary; no executor |
| `result_decision.py`, `publication_decision.py` | `application/result_assessment.py`, `application/publication_assessment.py` | preserve non-grant behavior |

## Interface boundary

```text
src/aos02/interfaces/cli.py
  -> parse arguments and choose use case
  -> serialize a structured result
  -> map result category to documented exit code
```

`interfaces/cli.py` may not decide record semantics, trust, path portability, baseline equality, or approval.

## Compatibility decision

```yaml
v2_record_schema_compatibility: REQUIRED
v1_implicit_migration: FORBIDDEN
legacy_v1_execution_eligibility: false
existing_command_names: PRESERVE_UNTIL_R6_CUTOVER
existing_command_exit_matrix: PRESERVE_UNTIL_R6_CUTOVER
runtime_mutation: FORBIDDEN
Git_write: FORBIDDEN
```

R2 must first keep current externally documented command behavior behind adapter-compatible module boundaries. Rename/removal of existing commands requires a separate compatibility decision plus CLI migration tests.

## Existing test migration map

| Existing tests | Target test layer |
|---|---|
| `test_canonical.py`, `test_validation.py`, `test_runtime_records.py`, `test_task_brief.py` | domain and application unit tests |
| `test_strict_loader.py`, `test_runtime_schema_v2.py`, `test_runtime_schema_contracts.py` | infrastructure contract tests |
| `test_execution*.py`, `test_result_decision.py`, `test_publication_decision.py`, `test_git_preflight.py` | application/infrastructure integration tests |
| `test_cli*.py` | interface/CLI integration tests |
| documentation tests | documentation navigation/contract tests |

## R2 exact change boundary

R2 may create the four target directories and move/add adapter implementations only when each move is backed by existing or new behavior-preserving tests.

```yaml
allowed_R2_areas:
  - src/aos02/domain/**
  - src/aos02/application/**
  - src/aos02/infrastructure/**
  - src/aos02/interfaces/**
  - src/aos02/__main__.py
  - tests/**
  - docs/reports/rebuild-program/**
forbidden_R2_features:
  - mutating_executor
  - trusted_identity
  - Git_write
  - push_merge_release_automation
  - network_services
  - UI
  - RAG
```

## R2 acceptance criteria

1. The current v2 bundle remains fail-closed for malformed, unknown, stale, untrusted, and blocked input.
2. All existing documented command exits retain their meaning.
3. No path is written by `execute-scoped`, preview, or validation.
4. CLI subprocess tests run through a declared installed/bootstrap package path, not hidden `PYTHONPATH`.
5. A full candidate report records all `NOT_RUN`, unknowns and bootstrap limitations.
