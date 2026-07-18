# AOS-02 A1-RMI Mutation Reachability Inventory v1

```yaml
document_type: A1_READ_ONLY_MUTATION_REACHABILITY_INVENTORY
project: AOS-02
repository: NMF13579/AOS-02
document_status: DRAFT
stage_id: A1-RMI-I
stage_completion_status: COMPLETE
control_status: HUMAN_REVIEW_REQUIRED

execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

## 1. Purpose and boundary

This report records the A1-RMI-I read-only discovery of filesystem-mutation reachability and current CLI/Python output behaviour in the inspected AOS-02 runtime baseline.

It is an audit artifact, not a Human Decision Record, Task Brief, Risk Profile assignment, implementation authorization, commit authorization, or evidence of trusted human authority. It does not grant execution, Git, publication, merge, or release authority.

Audit boundary:

```yaml
repository_mutation_allowed: false
production_mutation_allowed: false
network_access: disabled
real_production_write_during_trace: false
commit_created: false
```

## 2. Inspected runtime baseline

```yaml
inspected_runtime_baseline:
  repository: NMF13579/AOS-02
  branch: build/aos02-executable-control-core
  commit_oid: c878972e269b8ca9605aef659a815947832d0ac9
  tree_oid: 98901ef48f2eaeb1538cc37e7464935bad197677

relevant_runtime_subject_manifest:
  repository: NMF13579/AOS-02
  source_commit_oid: c878972e269b8ca9605aef659a815947832d0ac9
  source_tree_oid: 98901ef48f2eaeb1538cc37e7464935bad197677
  src_aos02_tree_oid: c588375a0e5ac1bb973dfdfdb89c5614d798e18b
  tests_tree_oid: e43db5a974d10fd2b635c19a74166a9451e6e388
  pyproject_blob_oid: d9d11f11b6625636d7806ca36857c6b7d619757c
  runtime_docs_tree_oid: a900db70104b65c04296444f598dbf4a23b2810b
  command_entrypoint_blob_oid: b347a010c14f480fb6de0e2ddd4878cf56547e08
  manifest_sha256: 60e58c955a55330c831dd6c580ca3b2e77fd46f5c0f91d481090066e6f6a2836
```

The manifest is the exact A1 runtime subject. A documentation-only commit may be used as an implementation parent only if this manifest remains identical.

## 3. Assurance method

### Static analysis

The audit inspected:

- package CLI entrypoint declared by `pyproject.toml`: `aos02 = aos02.__main__:main`;
- all Python modules below `src/aos02/`;
- direct mutation primitives: `Path.mkdir`, `tempfile.mkstemp`, `os.fdopen(..., "w")`, `os.replace`, and `Path.unlink`;
- wrappers and call chains around Evidence persistence and operation writes;
- CLI dispatch from `aos02.__main__.main()`;
- Python direct-executor callers in tests;
- import-time code, Git preflight and subprocess/Git-helper references.

### Dynamic trace

A non-mutating in-memory trace used a replacement for `_atomically_write_text` that recorded a target and raised `ValueError("WRITE_INTERCEPTED")` before any filesystem primitive could run. The trace exercised:

- direct execution with a locally valid-looking `HUMAN_OWNER` decision;
- direct execution with `DENY`;
- CLI `execute-scoped` dispatch with in-memory records;
- all seven documented CLI commands with in-memory records and no bundle-file creation.

No production write was allowed. The temporary roots used solely as non-existing path values remained absent after the trace.

## 4. Supported entrypoint inventory

| Entrypoint | Role | Filesystem mutation reachable |
|---|---|---|
| `aos02` / `aos02.__main__:main` | Package CLI dispatcher | Yes, through `execute-scoped` |
| `execute_scoped_request()` | Direct Python execution API | Yes |
| `preview_scoped_execution()` | Preview API | No |
| `validate_human_execution_decision()` | Execution-decision evaluation | No; but it currently accepts local authority claims |
| `validate_bundle()` | Canonical bundle validation | No |
| `compile_task_brief()` | Draft Task Brief compiler | No |
| `validate_human_result_decision()` | Result decision evaluation | No |
| `validate_human_publication_decision()` | Publication decision evaluation | No |
| `evaluate_git_preflight()` | Git-state evaluation | No |

Direct production executor callers were also found in `tests/test_execution.py` and `tests/test_cli_execution_preview.py`.

## 5. Mutation reachability inventory

### MP-01 — operation write after local declared authority

```yaml
entrypoint: execute_scoped_request
source:
  path: src/aos02/execution.py
  symbol: _atomically_write_text
call_chain:
  - execute_scoped_request
  - _atomically_write_text
  - Path.mkdir
  - tempfile.mkstemp
  - os.fdopen_write
  - os.replace
  - Path.unlink
reachable: true
reachable_without_trusted_authority: true
```

A local record containing `decided_by: HUMAN_OWNER` and `decision_value: ALLOW_LOCAL_EXECUTION` currently produces `valid: true` and `local_execution_authorized: true`. No trusted external identity or authority verifier is involved.

### MP-02 — blocked outcome Evidence persistence

```yaml
entrypoint: execute_scoped_request
source:
  path: src/aos02/execution.py
  symbols:
    - _persist_outcome
    - _persist_evidence
    - _atomically_write_text
call_chain:
  - execute_scoped_request
  - preview_scoped_execution
  - _persist_outcome
  - _persist_evidence
  - _atomically_write_text
  - .aos02/evidence-report.json
reachable: true
reachable_without_trusted_authority: true
```

A denied or otherwise blocked request reaches Evidence persistence. Therefore a blocked outcome can create `.aos02/evidence-report.json` even when no requested operation is performed.

### MP-03 — CLI dispatch to executor

```yaml
entrypoint: aos02 execute-scoped
source:
  path: src/aos02/__main__.py
  symbol: main
call_chain:
  - main
  - execute_scoped_request
  - MP-01_or_MP-02
reachable: true
reachable_without_trusted_authority: true
```

## 6. Dynamic trace evidence

```yaml
intercepted_write_targets:
  - /private/tmp/a1-rmi-no-write-sandbox/docs/example.md
  - /private/tmp/a1-rmi-no-write-sandbox/.aos02/evidence-report.json
  - /private/tmp/a1-rmi-cli-root/docs/example.md

post_trace_paths:
  /private/tmp/a1-rmi-no-write-sandbox: ABSENT
  /private/tmp/a1-rmi-cli-root: ABSENT
  repository/.aos02: ABSENT

repository_worktree_after_trace: CLEAN
```

The denied direct execution intercepted the attempted write of `.aos02/evidence-report.json`. The authorized-looking direct and CLI paths intercepted the requested operation target. The interceptor prevented all actual writes.

## 7. Current output compatibility inventory

All commands below were called through the current `main()` dispatcher with in-memory records. Every observed command returned exit `0`.

| Command | Observed current result |
|---|---|
| `validate` | Valid bundle returns `CONTROL_HUMAN_REVIEW_REQUIRED` and no approval grant. |
| `compile-task` | Returns `TASK_BRIEF` with `status: DRAFT`; authority fields remain false. |
| `validate-execution` | Locally declared `HUMAN_OWNER` returns `valid: true` and `local_execution_authorized: true`. |
| `preview-execution` | Valid-looking local authority returns `PREVIEW_READY`, `will_modify_files: false`. |
| `execute-scoped` | Routes to the mutation path; interception converts it to a caught bundle error while CLI still returns `0`. |
| `validate-result` | Structurally valid result decision returns `valid: true`; no Git authority is granted. |
| `validate-publication` | Structurally valid publication decision returns `valid: true`; no Git authority is granted. |

The existing exception handler in `main()` emits JSON `FAIL` / `CONTROL_BLOCKED` outcomes but returns `0`. This is a compatibility baseline to be deliberately changed by later command-specific exit-code work.

## 8. Containment implications

The common runtime write primitive is:

```yaml
primary_mutation_boundary:
  path: src/aos02/execution.py
  symbol: _atomically_write_text
```

Containment must occur before:

- `Path.mkdir`;
- `tempfile.mkstemp`;
- `os.fdopen(..., "w")`;
- `os.replace`;
- Evidence persistence;
- the operation loop.

The containment design must block both requested operation writes and blocked-outcome Evidence writes. It must not rely only on preview behaviour or on local `HUMAN_OWNER` fields.

Proposed future A1 source scope, subject to separately accepted Task Brief:

```yaml
production:
  - src/aos02/execution.py
  - src/aos02/__main__.py
  - src/aos02/execution_decision.py
  - src/aos02/execution_preview.py

tests:
  - tests/test_execution.py
  - tests/test_cli_execution_preview.py
  - tests/test_execution_decision.py
  - tests/test_execution_preview.py
  - tests/test_cli_execution_decision.py

documentation:
  - README.md
  - docs/runtime/executable-control-core.md
  - tests/test_runtime_documentation.py
```

This is an inventory-derived proposal only. It is not an accepted allowlist and does not authorize implementation.

## 9. Environment and limitations

```yaml
developer_bootstrap_status: NOT_VERIFIED
clean_installation: NOT_RUN
network_used: false
```

The existing `.venv/bin/python` did not import `aos02` without `PYTHONPATH=src`, so the existing environment does not prove the documented clean bootstrap path. No dependency installation or network access was attempted during this audit.

Limitations:

- This is reachability assurance over the inspected runtime subject, not a claim that no future code path can mutate files.
- Dynamic tracing intercepted the lowest write wrapper before real mutation; it did not execute filesystem writes.
- No trusted human authority, schema-v2 policy, strict parser, transaction recovery, or mutating executor was implemented or evaluated as accepted functionality.

## 10. Completion and next action

```yaml
all_supported_entrypoint_mutation_paths_accounted_for: true
unresolved_reachability: []
A1_RMI_report_accepted: false
A1_Task_Brief_materialization_ready: false

next_required_action: HUMAN_REVIEW_AND_AUTHORIZE_A1_RMI_C_ONLY
```

The only next action is a human decision whether to authorize a documentation-only local commit of this exact report. No implementation, code mutation, Task Brief materialization, push, merge, or release is authorized.
