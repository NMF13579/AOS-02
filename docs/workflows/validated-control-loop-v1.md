# Validated Control Loop v1

```yaml
workflow_status: IMPLEMENTED_NON_MUTATING
canonical_authority: NONE
execution_authorized: false
trusted_human_authority: NOT_IMPLEMENTED
mutating_executor: DISABLED
```

## Purpose

This is the executable vertical slice of the rebuilt control core. It turns a local canonical bundle into one of three kinds of result:

1. a deterministic technical validation result;
2. a **DRAFT-only** Task Brief compilation result;
3. a non-mutating execution preview or an explicitly blocked execution result.

Nothing in this loop is a human approval or a Git authorization.

## Control flow

```text
Idea + Risk + Scope
  -> compile-task (DRAFT only)
  -> Task + Evidence
  -> validate (technical result only)
  -> local Human Execution Decision + Execution Request
  -> preview-execution (exit 4, readiness blocked)
  -> execute-scoped (exit 4, mutation disabled)
```

## Run the supported local path

```bash
python3.11 -m venv .venv
.venv/bin/pip install ".[test]"
.venv/bin/python -m pytest
```

The package embeds the runtime v2 schemas needed by installed CLI subprocesses. A normal installation, not an editable-only assumption, is the supported baseline.

## Required interpretation

| Command outcome | Meaning | Does **not** mean |
|---|---|---|
| `validate` exit 0 | Records are technically valid | Approved or executable |
| `compile-task` exit 0 | A draft was compiled | Execution authorized |
| `validate-execution` exit 4 | Local decision structure was evaluated; authority is untrusted | Human authority exists |
| `preview-execution` exit 4 | Preview produced; readiness is blocked | Mutation can proceed |
| `execute-scoped` exit 4 | Mutating executor is disabled | Request was executed |

## Explicit boundary

The filesystem must remain unchanged for `preview-execution` and `execute-scoped`. Future mutating execution needs a separate architecture decision, trusted authority source, transactional executor, recovery strategy, Task Brief, and validation matrix.
