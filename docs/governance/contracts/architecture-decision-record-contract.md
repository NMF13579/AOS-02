# Architecture Decision Record Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_ARCHITECTURE_DECISION_RECORD_SEMANTICS_ONLY`

**Accepted by:** Human Owner via bounded batch decision `AOS02-REF-P7-10-BATCH-001`  
**Accepted at:** `2026-07-17T20:01:14Z`

## Purpose

An Architecture Decision Record (ADR) records a proposed or accepted bounded architecture decision, its alternatives, trade-offs, consequences, and evidence. An ADR does not implement itself and cannot authorize code, migration, runtime enforcement, or release.

## Required fields
ADR identity, decision question, context, alternatives considered, recommended option, trade-offs, consequences, dependencies, evidence, open questions, and a separate Human Decision Record binding for acceptance.

## Status rules
`PROPOSED` is not accepted. `HUMAN_ACCEPTED` requires explicit human decision bound to a specific ADR revision. A superseded or revoked ADR must not silently govern new work. Unknown implications or missing alternatives require `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED`.

## Authority boundary

This contract defines only AOS-02 architecture_decision_record semantics. It does not authorize implementation, runtime enforcement, any live system change, legacy reuse/migration, or Git/release action. Templates and examples have no authority.

## Dependencies

Human Decision Record, Task Brief, Evidence Report, Status & Glossary, Risk Profile, Scope & Change, and Delivery contracts.

## Acceptance boundary

Any future modification requires a new explicit Human Decision Record.
