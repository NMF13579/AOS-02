# AOS-02 Documentation Navigation

```yaml
artifact_role: DOCUMENTATION_NAVIGATION
canonical_authority: NONE
changes_source_precedence: false
grants_authority: false
grants_execution_authorization: false
grants_approval_authority: false
```

This page is a navigation aid for the current AOS-02 repository. It does not replace, amend, rank, or accept the documents it links to. Follow each linked artifact for its own status and authority boundary.

## Current starting points

| Material | Role | Status | Link |
|---|---|---|---|
| Product Contract | Product intent and first-release boundary | `CURRENT_ACCEPTED` | [Open](product/product-contract.md) |
| Foundational Contract Integration Map | Relationship among accepted foundational contracts | `CURRENT_ACCEPTED` | [Open](architecture/foundational-contract-integration-map.md) |
| Governance Contracts | Canonical contracts for decisions, task briefs, evidence, risk, scope, delivery, and ADRs | `CURRENT_ACCEPTED` | [Open](governance/README.md) |
| Manual workflow | Idea → Task Brief → Evidence → Human Review workflow | `CURRENT_ACCEPTED` | [Open](workflows/idea-to-review-v0.md) |
| Executable Control Core | Local validator, preview, schemas, and explicit non-mutating execution boundary | `CURRENT_VERIFIED_STATE` | [Open](runtime/executable-control-core.md) |
| Runtime mapping v2 | Canonical contract to runtime representation mapping | `CURRENT_VERIFIED_STATE` | [Open](runtime/canonical-contract-runtime-mapping-v2.md) |
| Human review packet | Review-oriented explanation of the manual workflow | `EVIDENCE` | [Open](reviews/manual-control-workflow-v0-human-review.md) |
| Architecture decisions | Location and boundary for future ADRs | `CURRENT_ACCEPTED` | [Open](decisions/README.md) |

## Manual workflow aids

These templates reduce repeated formatting work. They are not records, registries, approvals, execution grants, or sources of authority.

| Template | Role | Status | Link |
|---|---|---|---|
| Task Brief template | Manual starting point for a bounded task | `TEMPLATE` | [Open](templates/task-brief-template.md) |
| Stage report template | Manual report format for one completed stage | `TEMPLATE` | [Open](templates/stage-report-template.md) |

## Fictional manual demonstration

| Material | Role | Status | Link |
|---|---|---|---|
| Manual Workflow Demonstrator v0 | Fictional, non-authoritative walkthrough of the complete documentation/control chain | `READ_ONLY_REFERENCE` | [Open](examples/manual-workflow-v0/README.md) |

## Known limitations

- The executable control core is deliberately non-mutating.
- Trusted human authority is not implemented.
- A technical PASS, Evidence, template, local record, or agent output is not approval or authorization.
- This navigation page does not grant commit, push, merge, release, or execution authority.

## Historical reference

AOS-FARM materials and historical source packs are read-only reference material. They may inform questions and lessons, but they are not current AOS-02 authority and are not imported by this navigation layer.

## Next product work

Future work must derive from the current Product Contract and a separately accepted, bounded Task Brief. This page does not create a roadmap or authorize that work.
