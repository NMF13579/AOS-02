# Evidence Report Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_EVIDENCE_REPORT_SEMANTICS_ONLY`

**Accepted by:** Human Owner  
**Accepted at:** `2026-07-17T19:52:27Z`

## Purpose

An Evidence Report records observed technical facts for one bounded Task Brief: what changed, what was checked, what was not checked, and what remains unknown or blocked. It is not a human decision and cannot grant authority.

## Mandatory semantics

```text
Evidence ≠ approval
Evidence ≠ execution authorization
PASS ≠ approval
NOT_RUN ≠ PASS
UNKNOWN ≠ OK
Missing evidence ≠ no evidence needed
```

## Required fields

| Field | Requirement |
|---|---|
| `evidence_report_id` | Stable identity |
| `task_brief_binding`, `baseline_binding` | Exact work/state binding |
| `scope_observation` | Changed items and out-of-scope observation |
| `checks` | Exact command/check, result, exit code, output reference, status |
| `evidence_artifacts` | Path, digest, source observation, verification result |
| `claims` | Claim → artifact → verification method → status |
| `unknowns`, `not_run`, `blockers` | Explicit lists; empty only when observed empty |
| `technical_status` | `PASS`, `FAIL`, `BLOCKED`, `UNKNOWN_BLOCKED`, `NOT_RUN`, or `HUMAN_REVIEW_REQUIRED` |
| `authorization_boundary` | All non-evidence grants remain explicit and separate |

## Binding and freshness

Evidence must identify the Task Brief and applicable baseline. A change to the relevant scope, baseline, candidate set, required validation, or evidence artifact makes prior evidence stale until re-observed. A digest alone proves only byte identity of an artifact; it does not prove a human decision, completeness, correctness of a claim, or runtime enforcement.

## Failure behaviour

A required missing check, missing evidence, required `NOT_RUN`, unknown binding, stale baseline, or contradiction between claim and observed artifact results in `BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED`, not unqualified PASS.

## Authority boundary

An Evidence Report may support human review but cannot create execution, commit, push, merge, release, lifecycle, risk, scope-expansion, or result-acceptance authority. Each requires a separately scoped Human Decision Record.

## Template and example boundary

Template completion and the example create no real evidence and no authority.

## Dependencies

This candidate depends on the accepted Human Decision Record and Task Brief contracts. It does not extend either contract's authority.

## Acceptance boundary

This contract is accepted only for AOS-02 Evidence Report semantics. It does not create a real evidence claim, authorize execution, implementation, runtime enforcement, legacy reuse, migration, or any Git/release operation. Future changes require a new human decision record.
