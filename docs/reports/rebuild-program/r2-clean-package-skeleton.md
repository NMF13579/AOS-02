# R2 — Clean Package Skeleton and Deterministic Core

```yaml
stage: R2
status: COMPLETE
baseline_commit: f427d189aad94f386cc5bc9433fce64f2c6c899d
implementation_type: BEHAVIOR_PRESERVING_MODULAR_REORGANIZATION
runtime_mutation: false
Git_write: false
trusted_authority: false
full_test_result: PASS
full_test_count: 80
next_required_action: R3_SCOPED_WORKFLOW_VERTICAL_SLICE
```

## Delivered boundaries

```text
src/aos02/
  domain/
    canonical.py
  application/
    control_validation.py
    task_compilation.py
    execution_control.py
    decision_assessment.py
  infrastructure/
    strict_yaml.py
    schema_registry.py
  interfaces/
    cli.py
```

The old root modules remain intentionally as compatibility adapters where their import path or monkeypatchable constants are part of existing test behavior. `__main__.py` is now a minimal module entrypoint that delegates to `interfaces.cli.main`.

## Preserved behavior

- strict YAML rejection, resource limits and v2 schema validation;
- fail-closed bundle validation;
- current CLI commands and exit code behavior;
- non-mutating execution/preview boundary;
- no Git authority, execution authority, merge or release authority;
- existing root import compatibility for tests and callers.

## Validation

| Check | Result |
|---|---|
| Strict loader + R2 boundary tests | PASS — 18 passed |
| Installed-package schema resource lookup | PASS — schemas packaged under `aos02/schema_data` |
| Local wheel installation without dependencies | PASS — `pip install --force-reinstall --no-deps .` |
| Full suite after installed package validation | PASS — 80 passed |
| Runtime mutation/Git writes introduced | NO |

## Bootstrap note

The pre-R2 suite had 8 failing CLI subprocess tests because `aos02` was not installed in the existing `.venv`. The initial editable-install attempt was not durable in this host environment: a later interpreter did not process its generated path file. R2 therefore packages the v2 schemas as application data and validates a normal local wheel installation with `--no-deps`; the installed CLI subprocess suite now passes. R4 still requires a fresh isolated clean-install verification and published developer instructions.

## Non-grants

This structural change does not approve a result, authorize execution, create trusted human identity, enable filesystem mutation, or authorize commit/push/merge/release.
