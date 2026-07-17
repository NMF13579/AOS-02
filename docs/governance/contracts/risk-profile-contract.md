# Risk Profile Contract

**Status:** `HUMAN_ACCEPTED` · `CANONICAL_AOS_02_CONTRACT_FOR_RISK_PROFILE_SEMANTICS_ONLY`

**Accepted by:** Human Owner via bounded batch decision `AOS02-REF-P7-10-BATCH-001`  
**Accepted at:** `2026-07-17T20:01:14Z`

## Purpose

Risk Profile assigns the required control depth to one bounded Task Brief. Assignment is a separate human decision; an agent, technical PASS, or Evidence Report cannot assign, lower, or waive a profile.

## Levels

| Level | Intended scope | Minimum control |
|---|---|---|
| `LOW_RISK_FAST` | Narrow, reversible documentation-only work | Explicit Task Brief, validation/evidence, human review where required |
| `MEDIUM` | Bounded materialization with meaningful contract/process impact | Explicit scope/baseline, validation/evidence, execution decision, human review |
| `HIGH_RISK_PROTECTED` | Authority, enforcement, identity, destructive, release, or high-impact change | Stronger independent review, explicit gates, no silent downgrade |

## Assignment rules
A profile record must bind task, baseline, rationale, selected level, required controls, and non-grants. If classification is uncertain or the scope expands, use `UNKNOWN_BLOCKED` or reassign upward through a new human decision. Risk may not be lowered by narrative or a passing check.

## Authority boundary

This contract defines only AOS-02 risk_profile semantics. It does not authorize implementation, runtime enforcement, any live system change, legacy reuse/migration, or Git/release action. Templates and examples have no authority.

## Dependencies

Human Decision Record, Task Brief, and Status & Glossary contracts.

## Acceptance boundary

Any future modification requires a new explicit Human Decision Record.
