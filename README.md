# AOS-02

AOS-02 is a greenfield, human-governed AI engineering control core.

This repository provides a local validator, draft Task Brief compiler, scoped execution preview, runtime schema contracts, and CI test configuration. Its execution endpoint is deliberately non-mutating until trusted human authority and a bounded mutating executor are separately implemented. It has no authority for autonomous execution, Git operations, publication, merge, release, or human approval.

## Canonical starting documents

- [Product Contract](docs/product/product-contract.md)
- [Foundational Contract Integration Map](docs/architecture/foundational-contract-integration-map.md)
- [Governance Contracts](docs/governance/README.md)
- [Manual Control Workflow v0](docs/workflows/idea-to-review-v0.md)
- [Validated Control Loop v1](docs/workflows/validated-control-loop-v1.md)
- [Executable Control Core](docs/runtime/executable-control-core.md)
- [Human Usability Review Packet](docs/reviews/manual-control-workflow-v0-human-review.md)
- [V0 Closeout Human-Review Checklist](docs/reviews/v0-closeout-human-review-checklist.md)

## Verified local command path

Use the clean-environment command sequence in the [Executable Control Core runtime guide](docs/runtime/executable-control-core.md#run-locally). It installs the declared test dependencies, exercises every v0 CLI command, uses an explicit sandbox root for the sole real execution command, and runs the full test suite.

## Important boundaries

- AOS-FARM is a read-only reference source and is not imported as product code.
- Technical evidence is not human approval.
- A Task Brief is not execution, commit, push, merge, or release authority.
- This documentation baseline is committed and published on `main`; every future change still requires a separately scoped Human Decision Record.
