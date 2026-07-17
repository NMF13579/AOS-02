# Idea → Human Review v0

**Status:** `DOCUMENTATION-ONLY WORKFLOW`

This is the first usable AOS-02 workflow. It is performed manually in Markdown/YAML. No template, example, check, or agent output grants permission by itself.

## Purpose

Turn a vague idea into an inspectable record of: what was proposed, what was allowed, what was observed, what remains unknown, and what a human decided.

## Route

1. **Record the idea** — create an `idea-record.yaml`. State the problem, desired outcome, and known unknowns. Do not write a Task Brief yet.
2. **Choose risk and scope** — a human selects the Risk Profile and approves the Scope & Change record. If the scope is unclear, stop.
3. **Draft a Task Brief** — bind it to the idea, risk, scope, baseline, allowed operations, evidence requirements, and stop conditions.
4. **Grant or deny execution explicitly** — use a Human Decision Record. Without `HUMAN_ACCEPTED` execution authority, work is blocked.
5. **Perform only the allowed work** — record checks, changed artifacts, `NOT_RUN`, and unknowns in an Evidence Report.
6. **Human review** — the human accepts, rejects, or requests changes. Technical PASS is evidence, never approval.

## Fail-closed rules

```text
missing binding → BLOCKED
uncertain or expanded scope → reassess risk and scope
missing execution decision → do not perform work
NOT_RUN / UNKNOWN → never report PASS
evidence → never becomes approval
```

## First-release boundary

This workflow deliberately does not include runtime enforcement, CI, databases, web UI, autonomous execution, or automatic Git operations. Those are later architecture decisions, not prerequisites for learning whether the workflow helps a human.

## Completion test

A reviewer who did not participate can follow the IDs and references from the example’s idea through the final decision, identify every unknown, and see exactly which decisions were human decisions.
