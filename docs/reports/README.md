# AOS-02 Project Reports

```yaml
artifact_role: PROJECT_REPORT_INDEX
canonical_authority: NONE
grants_execution_authorization: false
grants_commit_authorization: false
grants_push_authorization: false
grants_merge_authorization: false
grants_release_authorization: false
```

This directory stores versioned, repository-local technical reports for completed AOS-02 stages. It is the canonical project location for implementation, preflight, and validation reports so that a reader can inspect the evidence next to the code and documentation it describes.

A report records observations. It does **not** grant authority, accept a result, authorize execution, or authorize a Git action. Read the linked Task Brief, Human Decision Record, and review material separately where they exist.

## Current reports

| Stage | Report | Technical outcome | Next action recorded in the report |
|---|---|---|---|
| S1 — Documentation Navigation | [Implementation and Validation Report](s1-documentation-navigation/implementation-validation-report.md) | `PASS` | `HUMAN_REVIEW_OF_LOCAL_S1_CANDIDATE` |
| S2 — Manual Workflow Demonstrator | [Implementation and Validation Report](s2-manual-workflow-demonstrator/implementation-validation-report.md) | `PASS` | `HUMAN_REVIEW_OF_LOCAL_S2_CANDIDATE` |
| S3 — Project Reports Baseline | [Implementation and Validation Report](s3-project-reports-baseline/implementation-validation-report.md) | `PASS` | `HUMAN_REVIEW_OF_LOCAL_S3_CANDIDATE` |
| Rebuild Program | [Reference audit and staged rebuild plan](rebuild-program/README.md) | `PLANNING_BASELINE` | `R1_TARGET_CONTRACT_CONSOLIDATION` |

## Storage policy

- Store reports that describe repository state, validation, candidate identity, limitations, `NOT_RUN`, unknowns, or blockers under `docs/reports/`.
- Keep formal human review packets and acceptance/checklist material in `docs/reviews/`.
- Store fictional walkthrough material in `docs/examples/`; it is not evidence for real work.
- A local Desktop copy may be used for delivery or drafting, but the committed file under this directory is the project-local reference.
- A report is immutable evidence for its recorded candidate. A later code or documentation change does not retroactively change that report; it requires a new report if new validation is claimed.
