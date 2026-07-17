# Foundational Contract Integration Map

**Status:** `HUMAN_ACCEPTED` · **Authorization:** `AOS02-REF-P11-14-BATCH-001`

## System intent
AOS-02 is a human-centred, documentation-first control workflow: **Idea → Task Brief → Evidence → Human Review**. It observes and advises; it does not autonomously execute. Markdown/YAML is canonical; storage/caches are derivative.

## Contract flow

```text
Idea / product need
  → ADR (when an architecture choice exists)
  → Risk Profile + Scope & Change
  → Task Brief
  → explicit Human Decision Record (execution only if separately granted)
  → Evidence Report
  → Delivery gates
  → explicit Human Decision Record (acceptance/delivery only if separately granted)
```

## Responsibility map

| Need | Canonical contract | Fail-closed rule |
|---|---|---|
| Who may decide | Human Decision Record | absent/expired/ambiguous → blocked |
| What work means | Task Brief | no brief/binding → no work claim |
| How risk is controlled | Risk Profile | uncertain/expanded scope → reassess |
| What can change | Scope & Change | out-of-scope → blocked |
| What happened technically | Evidence Report | NOT_RUN/UNKNOWN cannot become PASS |
| What statuses mean | Status & Glossary | ambiguity → UNKNOWN_BLOCKED |
| How delivery proceeds | Delivery | technical validation ≠ acceptance |
| Why an architecture choice exists | ADR | proposal ≠ implementation authority |

## Non-negotiable separation

```text
Agent output ≠ human decision
Technical PASS ≠ approval
Evidence ≠ authorization
Task Brief ≠ execution grant
ADR ≠ implementation authorization
Delivery ≠ release authorization
```

## Unresolved before implementation
Repository creation, implementation language/tooling, identity assurance, runtime enforcement, CI, data model, integrations, and release mechanics are intentionally outside this map and require later scoped decisions.
