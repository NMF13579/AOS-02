# Human Decision Record Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_HUMAN_DECISION_RECORD_SEMANTICS_ONLY`

**Accepted by:** Human Owner  
**Accepted at:** `2026-07-17T19:39:25Z`

## Purpose

A Human Decision Record makes one bounded decision by a human explicit and inspectable. It prevents a technical result, agent narrative, queue state, template, or Evidence Report from being mistaken for approval.

## Non-equivalences

```text
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval
Agent-generated record ≠ human decision
Template/example completion ≠ human decision
One grant ≠ any other grant
```

## Required record fields

| Field | Requirement |
|---|---|
| `decision_id` | Unique stable identifier |
| `decision_type` | Closed, explicit decision category |
| `decided_by` | Human reference; identity assurance level must be stated |
| `scope_binding` | Task/proposal/baseline/scope binding, where applicable |
| `decision_value` | Explicit accepted/rejected/needs-changes value |
| `grants` | Exact finite list; empty list is valid |
| `non_grants` | Explicitly says what is not allowed |
| `valid_from` / `expires_at` | Validity window; expiry is explicit if used |
| `single_use` / `consumed` | Replay semantics are explicit |
| `status` | `DRAFT`, `HUMAN_ACCEPTED`, `REJECTED`, `EXPIRED`, `CONSUMED`, or `REVOKED` |

## Candidate decision types

`TASK_SCOPE`, `RISK_PROFILE`, `EXECUTION`, `RESULT_ACCEPTANCE`, `COMMIT`, `PUSH`, `MERGE`, `RELEASE`, `ARCHITECTURE_DECISION`.

A decision type does not grant anything on its own. A record must state exact grants and non-grants.

## Validity and failure semantics

A record is not usable when missing, ambiguous, unbound to the required scope/baseline, expired, consumed, revoked, or not `HUMAN_ACCEPTED`. In these states the safe outcome is `BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED`; continuation must not be inferred.

Execution, commit, push, merge, release, scope expansion, risk assignment, result acceptance, and architecture acceptance are separate grants. A result-acceptance decision never implicitly grants a Git or release action.

## Identity boundary

The initial documentation-stage model is only `LOCAL_DECLARED_HUMAN_REFERENCE`. It is not a cryptographic, platform-authenticated, or independent trust claim. The identity/witness mechanism remains an explicit unresolved architecture/security decision.

## Template and example boundary

`templates/` is a drafting aid. `examples/` is illustrative only. Neither has authority, and neither may be treated as a decision record unless a separately identified human creates and accepts a scoped record.

## Evidence links

- `architecture/architecture-contract.md` — human authority and typed-grant candidate boundary.
- `product-reconstruction/product-contract.md` — human-centred product semantics.
- `reports/program-1/traceability-matrix.yaml` — evidence baseline links.

## Acceptance boundary

This contract is accepted only for AOS-02 Human Decision Record semantics. It does not authorize implementation, runtime enforcement, identity assurance claims, legacy reuse, migration, or any Git/release operation. Future changes require a new human decision record.
