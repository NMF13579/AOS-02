# Status & Glossary Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_STATUS_AND_GLOSSARY_SEMANTICS_ONLY`

**Accepted by:** Human Owner  
**Accepted at:** `2026-07-17T19:57:24Z`

## Purpose

This contract defines unambiguous terms and status meanings for AOS-02 contracts, records, and reports. A status has only the meaning specified here; it cannot be upgraded by narrative, agent inference, or omission.

## Technical statuses

| Status | Meaning | Non-meaning |
|---|---|---|
| `PASS` | A specified technical check passed within its recorded scope/baseline | Not approval, authorization, completeness, or safety proof |
| `FAIL` | A specified check produced a failing result | Not a decision about remediation |
| `BLOCKED` | A known required prerequisite prevents progress | Not permission to bypass |
| `UNKNOWN_BLOCKED` | Required knowledge is missing, ambiguous, stale, or contradictory; progress is blocked | Not a warning or soft failure |
| `NOT_RUN` | A required check was not executed | Not PASS, not evidence of absence |
| `HUMAN_REVIEW_REQUIRED` | A human decision/review is required before proceeding | Not a self-approving queue state |

## Decision statuses

| Status | Meaning |
|---|---|
| `DRAFT` | Proposal; no authority |
| `HUMAN_ACCEPTED` | Explicit human acceptance within its recorded scope and validity |
| `REJECTED` | Explicit human rejection |
| `EXPIRED` | Validity window ended |
| `CONSUMED` | A single-use decision was used |
| `REVOKED` | Previously accepted decision was withdrawn |

## Glossary

- **approval:** explicit human decision to accept a bounded item; never inferred from technical status.
- **authorization / grant:** an explicit, scoped permission in a Human Decision Record.
- **non-grant:** an explicit statement that an action is not permitted.
- **evidence:** an observed technical fact or artifact; not approval.
- **claim:** an assertion that must identify supporting evidence and verification method.
- **baseline:** identified source/state to which scope, task, check, or evidence binds.
- **scope:** explicit boundary of permitted or observed work.
- **out-of-scope:** outside the currently bound scope.
- **stale:** no longer safely applicable because relevant binding changed.

## Precedence and invariants

```text
HUMAN_ACCEPTED is a decision status, not a technical status.
PASS is a technical status, not a decision status.
PASS ≠ approval.
Evidence ≠ approval.
NOT_RUN ≠ PASS.
UNKNOWN_BLOCKED ≠ OK.
Missing status ≠ PASS.
Ambiguous status → UNKNOWN_BLOCKED.
```

A technical PASS cannot override a missing, stale, expired, revoked, or out-of-scope human decision. A human decision cannot erase a failed or not-run check; it may only state its own explicit decision.

## Template and example boundary

The template documents the vocabulary; the example is illustrative. Neither changes real status or grants authority.

## Dependencies

This candidate aligns terminology for the accepted Human Decision Record, Task Brief, and Evidence Report contracts; it does not modify their accepted clauses.

## Acceptance boundary

This contract is accepted only for AOS-02 status and glossary semantics. It changes no live system status and does not authorize implementation, runtime enforcement, legacy reuse, migration, or any Git/release operation. Future changes require a new human decision record.
