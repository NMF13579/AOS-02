# Stage Report Template

```yaml
artifact_role: MANUAL_TEMPLATE
canonical_authority: NONE
approval_effect: none
grants_authority: false
```

> A report records observations from one stage. A technical PASS and Evidence are not human approval or authorization.

```yaml
task_id: REQUIRED
stage: REQUIRED
subject_identity: REQUIRED
repository_identity: REQUIRED
baseline: REQUIRED
active_scope: REQUIRED

files_created: []
files_modified: []
files_inspected: []
forbidden_paths_touched: []
commands_run: []
validation_results: []
NOT_RUN: []
unknowns: []
limitations: []

technical_status: REQUIRED
control_status: HUMAN_REVIEW_REQUIRED
approval_effect: none
next_required_action: REQUIRED
```
