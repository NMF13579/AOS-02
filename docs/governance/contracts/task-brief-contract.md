# Task Brief Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_TASK_BRIEF_SEMANTICS_ONLY`

**Accepted by:** Human Owner  
**Accepted at:** `2026-07-17T19:45:30Z`

## Purpose

A Task Brief describes one bounded item of proposed work. It makes purpose, scope, risk, evidence, and stop conditions explicit. It is not an authorization to start work or perform any Git/release action.

## Required fields

| Field | Requirement |
|---|---|
| `task_id`, `purpose` | Stable identity and bounded intent |
| `risk_profile_binding` | Reference to a separate human risk decision |
| `baseline_binding` | Repository/state reference where applicable |
| `allowed_scope`, `forbidden_scope` | Exact paths or semantic boundaries |
| `allowed_operations`, `forbidden_operations` | Explicit operation set |
| `acceptance_criteria` | Observable technical outcomes |
| `required_validation`, `required_evidence` | Required checks and artifacts |
| `unknowns`, `not_run`, `blockers` | Must remain explicit |
| `required_human_decisions` | Separate decision bindings for execution and later actions |
| `non_grants` | Explicitly states what is not authorized |

## Mandatory semantics

```text
Task Brief ≠ execution authorization
Task Brief ≠ human decision
Task Brief ≠ approval
Task Brief ≠ commit/push/merge/release authorization
PASS ≠ approval
UNKNOWN ≠ OK
NOT_RUN ≠ PASS
```

## Authorization boundary

A valid Task Brief may be a prerequisite for work, but execution requires a separate accepted Human Decision Record of type `EXECUTION`, bound to the same task and applicable baseline/scope. Commit, push, merge, release, lifecycle changes, and scope expansion require separate decisions.

If a required binding, scope, risk assignment, evidence requirement, or human decision is missing, ambiguous, stale, expired, or out of scope, the outcome is `BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED`. No authority may be inferred.

## Template and example boundary

The template is a drafting aid; the example is illustrative. Neither authorizes execution or creates a real task.

## Dependency

This candidate depends on the accepted `Human Decision Record Contract`; it does not extend its authority.

## Acceptance boundary

This contract is accepted only for AOS-02 Task Brief semantics. It does not authorize a real task, implementation, runtime enforcement, legacy reuse, migration, or any Git/release operation. Future changes require a new human decision record.
