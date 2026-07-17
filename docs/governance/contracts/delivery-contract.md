# Delivery Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_DELIVERY_SEMANTICS_ONLY`

**Accepted by:** Human Owner via bounded batch decision `AOS02-REF-P7-10-BATCH-001`  
**Accepted at:** `2026-07-17T20:01:14Z`

## Purpose

Delivery Contract describes how a bounded delivery moves through milestones and human gates. It makes completion conditions explicit without treating a technical milestone as product acceptance or release authorization.

## Candidate milestones
`PROPOSED` → `SCOPED` → `EXECUTION_AUTHORIZED` → `TECHNICALLY_VALIDATED` → `HUMAN_REVIEW_REQUIRED` → `HUMAN_ACCEPTED` → `DELIVERED`.

## Gate rules
Each transition names required inputs, evidence, decision type, and stop conditions. `TECHNICALLY_VALIDATED` is not `HUMAN_ACCEPTED`. Delivery, commit, push, merge, or release each require separately scoped Human Decision Records. Missing/stale evidence or decisions stops the transition fail-closed.

## Authority boundary

This contract defines only AOS-02 delivery semantics. It does not authorize implementation, runtime enforcement, any live system change, legacy reuse/migration, or Git/release action. Templates and examples have no authority.

## Dependencies

Human Decision Record, Task Brief, Evidence Report, Status & Glossary, Risk Profile, and Scope & Change contracts.

## Acceptance boundary

Any future modification requires a new explicit Human Decision Record.
