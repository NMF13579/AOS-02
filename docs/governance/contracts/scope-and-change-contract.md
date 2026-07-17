# Scope & Change Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_SCOPE_AND_CHANGE_SEMANTICS_ONLY`

**Accepted by:** Human Owner via bounded batch decision `AOS02-REF-P7-10-BATCH-001`  
**Accepted at:** `2026-07-17T20:01:14Z`

## Purpose

Scope & Change defines what a bounded Task Brief may affect and how change is detected and handled. It separates allowed paths/operations from observed changes and requires a named baseline.

## Required bindings
A scope record names task, baseline, allowed paths/semantic areas, forbidden paths/areas, allowed operations, forbidden operations, expected change set, and out-of-scope handling.

## Rules
Out-of-scope, unbound, stale, or ambiguous changes are `BLOCKED` or `UNKNOWN_BLOCKED`. A baseline change requires re-evaluation; a scope expansion requires a separate human decision and updated Task Brief. No diff, agent statement, or technical PASS authorizes scope expansion.

## Authority boundary

This contract defines only AOS-02 scope_and_change semantics. It does not authorize implementation, runtime enforcement, any live system change, legacy reuse/migration, or Git/release action. Templates and examples have no authority.

## Dependencies

Human Decision Record, Task Brief, Evidence Report, and Status & Glossary contracts.

## Acceptance boundary

Any future modification requires a new explicit Human Decision Record.
