# AOS-02 Canonical Product Contract

**Status:** `HUMAN_ACCEPTED` · **Authorization:** `AOS02-REF-P11-14-BATCH-001`

## Product identity
AOS-02 is a new, independent product. It is not a fork of AOS-FARM. AOS-FARM materials may be consulted as evidence only; code is not imported.

## Primary user and job
The primary user is a human responsible for AI-assisted engineering work who needs to know: *what is proposed, what is allowed, what was checked, what remains unknown, and which decision is still theirs.*

## First product outcome
A documentation/control workflow that makes **Idea → Task Brief → Evidence → Human Review** inspectable and fail-closed, without autonomous execution.

## Canonical state
Markdown and YAML are the source of truth. Databases, search indexes, UI projections, and caches—if later introduced—are derived and cannot silently override canonical records.

## First-release boundaries

| Included | Excluded |
|---|---|
| Human decisions, task briefs, evidence reports, risk/scope/delivery controls, ADRs | Autonomous execution, auto-commit/push/merge, release automation, enforced runtime blocking, identity claims, legacy migration |

## Success criteria
A human can reconstruct the chain from intent through scope, checks/evidence, unknowns, and explicit decisions; no technical result is misrepresented as approval.

## Non-goals
This contract does not choose an implementation stack, create a repository, authorize code, or claim a working product.
