# AOS-02 Reference-Driven Rebuild Program

```yaml
artifact_role: REBUILD_PROGRAM_INDEX
canonical_authority: NONE
implementation_status: PLANNING_BASELINE
execution_authorization: false
commit_authorization: false
push_authorization: false
merge_authorization: false
release_authorization: false
```

This directory holds the planning, audit, and later stage reports for the AOS-02 reference-driven rebuild. A rebuild stage starts only after its preceding stage has recorded an exact candidate and its required validation. Neither this index, a plan, a technical PASS, nor a report creates human/runtime authority.

## Current artifacts

| Artifact | Role | Status | Link |
|---|---|---|---|
| Reference audit | Read-only inventory and preserve/replace/avoid decision | `COMPLETE` | [Open](reference-audit.md) |
| Rebuild program plan | Target architecture, stages, boundaries, and stop conditions | `DRAFT_FOR_IMPLEMENTATION` | [Open](aos02-reference-driven-rebuild-plan.md) |
| R1 target contract consolidation | Domain/application/infrastructure/interface map and compatibility boundary | `COMPLETE` | [Open](r1-target-contract-consolidation.md) |
| R2 clean package skeleton | Behavior-preserving modular layout and deterministic core boundary | `COMPLETE` | [Open](r2-clean-package-skeleton.md) |
| R3 validated workflow vertical slice | Discoverable installed-package control loop and explicit blocked-execution boundary | `COMPLETE` | [Open](r3-validated-workflow-vertical-slice.md) |
| R4 clean install and bootstrap | Fresh non-hermetic installation, embedded schema check, CLI and full suite | `COMPLETE_NON_HERMETIC` | [Open](r4-clean-install-and-bootstrap.md) |
| R5 documentation and dogfood | Owner workflow, fictional example, documentation-only dogfood, and checklist | `COMPLETE` | [Open](r5-documentation-and-dogfood.md) |
