# Rebuild v1 — Human Acceptance for `dev`

```yaml
decision_type: HUMAN_REBUILD_CANDIDATE_ACCEPTANCE
decision_status: ACCEPTED
accepted_by: HUMAN_OWNER
accepted_at: 2026-07-18
candidate:
  branch: dev
  commit_oid: 94d46b430b2abb5aac97ea198fb103b6942d8904
  tree_oid: 73944db2fe51f854aeb93001fa877ec17cfd4ca2
accepted_scope: NON_MUTATING_CONTROL_CORE_V1
validation:
  local_full_suite: PASS
  independent_P0_review: PASS
limitations_accepted:
  - trusted_human_authority_not_implemented
  - mutating_executor_disabled
  - git_write_adapter_not_implemented
  - hermetic_reproducibility_not_validated

commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false

next_required_action: CONTINUE_DEVELOPMENT_ON_DEV
```

## Decision boundary

The human owner accepts this exact `dev` candidate as the stable development baseline. This is not authorization to merge into `main`, release, create Git authority, or enable mutating execution. Subsequent work remains on `dev` and requires its own validation and review before any future `main` merge decision.
