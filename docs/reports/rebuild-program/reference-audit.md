# AOS-02 Rebuild Reference Audit

```yaml
audit_id: AOS02-REBUILD-R0
status: COMPLETE
source_mode: READ_ONLY
reference:
  repository: NMF13579/AOS-FARM
  branch: main
  commit: c3b4f04bdaf504eb4e65d49f60bef92084e3aad0
  local_snapshot: /tmp/aos-farm-reference-audit
  authority: NONE
target:
  repository: NMF13579/AOS-02
  branch_at_audit: build/aos02-executable-control-core
  head_at_audit: dc8fcd33358ab1c7cb7d340569fe2321a27dd8b2
```

## Observed reference structure

The AOS-FARM snapshot contains a substantial reusable knowledge base, including:

| Area | Observed tracked files | Rebuild value |
|---|---:|---|
| `aos/` | 526 | Functional/reference patterns; not a copy target |
| `docs/` | 89 | Workflow, governance and assembly ideas |
| `templates/` | 89 | Candidate concepts/templates to selectively reimplement |
| `tests/` | 263 | Negative cases and acceptance ideas |
| `reports/` | 1149 | Historical evidence/examples; not target state |
| `tasks/` | 13 | Task representation ideas |

The reference's core control sources establish a documentation-first workflow, a Minimal Safety Floor, explicit human boundaries, and a distinction between reports/evidence and approval. Its `aos/` product kit is extensive and includes consumer documentation, schemas, scripts and optional tooling.

## Rebuild interpretation

AOS-FARM is valuable as **functional evidence**, not as a target codebase. Direct import would bring unrelated product boundaries, a large documentation surface, historical state, and its internal project-control hierarchy into AOS-02.

### Preserve

- Idea → scoped task → evidence → human review flow.
- `PASS ≠ approval`, `Evidence ≠ approval`, `UNKNOWN / NOT_RUN ≠ PASS`.
- Documentation-before-code sequencing.
- Read-only reference policy, explicit non-grants, and project-local reports.
- Negative validation as a first-class requirement.

### Replace

- The broad `/aos/` hierarchy with a compact AOS-02 modular package.
- AOS-FARM internal root control files with AOS-02's own accepted contracts.
- Large registry/queue surfaces with only the AOS-02 capabilities needed by the first owner workflow.

### Avoid

- Copying source files, historical reports, task queues or canonical AOS-FARM documents.
- Treating test success, agent output, local YAML or reference content as approval.
- Introducing automatic Git actions, execution mutation, trusted identity, UI, RAG or SaaS during the rebuild foundation.

## Current target strengths to retain

The audited AOS-02 baseline already has:

- a non-mutating executable control core;
- strict v2 schema direction and fail-closed CLI semantics;
- documented no-authority boundaries;
- fictional workflow examples;
- project-local reports.

The rebuild should retain these proven safety properties while replacing the prototype's internal organization with explicit domain/application/infrastructure/interface boundaries.

## Result

```yaml
rebuild_recommended: true
rebuild_style: REFERENCE_DRIVEN_REIMPLEMENTATION
reference_copying_allowed: false
first_implementation_stage: R1_TARGET_CONTRACT_CONSOLIDATION
human_review_required_before_cutover: true
```
