# Task Brief Template

```yaml
artifact_role: MANUAL_TEMPLATE
canonical_authority: NONE
grants_execution_authorization: false
grants_commit_authorization: false
grants_push_authorization: false
grants_merge_authorization: false
grants_release_authorization: false
```

> Copy and complete this template only for a separately bounded task. A completed template is still not authorization without the required human decision.

```yaml
task_id: REQUIRED
revision: REQUIRED
goal: REQUIRED
repository: REQUIRED
branch: REQUIRED
baseline:
  commit_oid: REQUIRED
  tree_oid: REQUIRED
subject_identity: REQUIRED

readable_paths: []
writable_paths: []
protected_no_write_paths: []
excluded_paths: []

allowed_operations: []
forbidden_operations: []
expected_created_paths: []
expected_modified_paths: []

validation_checks: []
stop_conditions: []
unexpected_change_behavior: STOP_AND_REPORT
expected_report: REQUIRED

commit_boundary: NOT_AUTHORIZED
push_boundary: NOT_AUTHORIZED
merge_boundary: NOT_AUTHORIZED
release_boundary: NOT_AUTHORIZED
non_grants:
  human_authority: false
  execution_authority: false
  commit_authority: false
  push_authority: false
  merge_authority: false
  release_authority: false
```
