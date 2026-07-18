# Canonical Contract to Runtime Mapping v2

**Status:** `MATERIALIZED_RUNTIME_MAPPING_V2`

**Applies to:** the AOS-02 non-mutating control core

**Runtime schema version:** `2.0`

This document maps the accepted AOS-02 canonical contract semantics into a
strict runtime representation. It does not amend the canonical contracts. If a
runtime rule conflicts with a canonical contract, the canonical contract wins
and runtime processing stops fail-closed.

## Safety and authority boundary

The runtime is an observer and validator. It does not implement trusted human
identity, trusted execution authority, a mutating executor, Git authority, or
release authority.

```text
schema PASS != technical PASS
technical PASS != approval
local HUMAN_ACCEPTED != trusted human authority
Evidence != approval or authorization
Task Brief != execution authorization
structurally valid execution decision + unavailable trusted authority -> BLOCKED
```

Every runtime result keeps `execution_authorized`, `commit_authorized`,
`push_authorized`, `merge_authorized`, and `release_authorized` false whenever
those fields are present. The `execute-scoped` API and CLI remain non-mutating:
they do not inspect or write the supplied root, create target paths, create
`.aos02`, persist Evidence, or create temporary files.

## Canonical source map

| Runtime concern | Canonical source | Runtime v2 rule |
|---|---|---|
| status vocabulary and precedence | `status-and-glossary-contract.md` | only canonical technical/decision statuses; ambiguity is `UNKNOWN_BLOCKED` |
| task identity and bounded scope | `task-brief-contract.md` | exact task, risk, scope, baseline, path, and check bindings |
| human decisions | `human-decision-record-contract.md` | local YAML is structural input only and has `LOCAL_DECLARED_HUMAN_REFERENCE` assurance |
| risk | `risk-profile-contract.md` | only `LOW_RISK_FAST`, `MEDIUM`, or `HIGH_RISK_PROTECTED`; selection is not trusted authority |
| scope and path change | `scope-and-change-contract.md` | portable relative paths, no collisions, and no allowed/forbidden overlap |
| evidence | `evidence-report-contract.md` | exact task/baseline binding; explicit checks, unknowns, not-run items, and blockers |
| later delivery actions | `delivery-contract.md` | result/publication validation never grants commit, push, merge, or release |

## Closed-world bundle and YAML rules

A bundle directory contains only regular, non-symlink `*.yaml` files whose
names are in this registry:

| File | Schema |
|---|---|
| `idea.yaml` | `idea-record-2.0.schema.json` |
| `risk.yaml` | `risk-profile-2.0.schema.json` |
| `scope.yaml` | `scope-and-change-2.0.schema.json` |
| `task.yaml` | `task-brief-2.0.schema.json` |
| `evidence.yaml` | `evidence-report-2.0.schema.json` |
| `execution-decision.yaml` | `human-execution-decision-2.0.schema.json` |
| `execution-request.yaml` | `execution-request-2.0.schema.json` |
| `result-decision.yaml` | `human-result-decision-2.0.schema.json` |
| `publication-decision.yaml` | `human-publication-decision-2.0.schema.json` |

Unknown files, subdirectories, `.yml`, symlinks, non-regular entries,
case-folded filename collisions, missing command-required records, duplicate
YAML keys, aliases, anchors, merge keys, custom tags, multiple YAML documents,
non-string mapping keys, empty documents, and non-mapping top-level documents
are rejected before semantic evaluation. All present records are validated,
including recognized records not consumed by the selected command.

Every v2 schema uses `additionalProperties: false`. A record must declare
`schema_version: "2.0"`; v1 and unversioned records are rejected rather than
implicitly upgraded.

## Runtime record map

The schemas under `schemas/runtime/` are the machine-readable closed-world
field definitions. The following table states the binding-bearing fields; the
schemas define their exact types, enums, required fields, and nested shapes.

| Record | Identity | Required exact bindings | Authority interpretation |
|---|---|---|---|
| `IDEA_RECORD` | `idea_id` | none | proposal only |
| `RISK_PROFILE` | `risk_id` | `idea_binding`, `baseline_binding` | local risk statement only |
| `SCOPE_AND_CHANGE` | `scope_id` | `idea_binding`, `baseline_binding` | scope description only |
| `TASK_BRIEF` | `task_id` | `idea_binding`, `risk_binding`, `scope_binding`, `baseline_binding` | bounded draft, never authority |
| `EVIDENCE_REPORT` | `evidence_id` | `task_binding`, `baseline_binding` | technical observations only |
| execution decision projection | `decision_id` | `scope_binding == task_id`, `baseline_binding` | structurally checkable, always authority `UNTRUSTED` |
| `EXECUTION_REQUEST` | no independent authority identity | `task_binding`, `baseline_binding` | requested operations only |
| result decision projection | `decision_id` | `scope_binding == task_id`, `evidence_binding`, `baseline_binding` | structurally recorded intent only; no implicit grant |
| publication decision projection | `decision_id` | `scope_binding == task_id`, `evidence_binding`, `baseline_binding` | structurally recorded intent only; all Git/release grants remain false |

The three decision projections use `record_type: HUMAN_DECISION_RECORD` and the
canonical decision types `EXECUTION`, `RESULT_ACCEPTANCE`, and `PUSH`. Separate
schemas keep command-specific decision values closed without inventing new
canonical authority categories.

## Exact cross-record bindings

For the full validation bundle:

```text
risk.idea_binding == idea.idea_id
scope.idea_binding == idea.idea_id
task.idea_binding == idea.idea_id
task.risk_binding == risk.risk_id
task.scope_binding == scope.scope_id
risk.baseline_binding == scope.baseline_binding == task.baseline_binding
evidence.task_binding == task.task_id
evidence.baseline_binding == task.baseline_binding
```

For execution commands:

```text
execution-decision.scope_binding == task.task_id
execution-decision.baseline_binding == task.baseline_binding
execution-request.task_binding == task.task_id
execution-request.baseline_binding == task.baseline_binding
```

For result and publication commands:

```text
decision.scope_binding == task.task_id
decision.evidence_binding == evidence.evidence_id
decision.baseline_binding == task.baseline_binding == evidence.baseline_binding
```

Missing, stale, ambiguous, or unequal bindings are semantic failures. Digest
comparison is not substituted for exact identifier equality, and identifier
equality is not treated as proof that a human decision is trusted.

## Portable paths and collision keys

Runtime paths use relative POSIX syntax. A portable path:

- is non-empty UTF-8 text already normalized to Unicode NFC;
- uses `/`, never `\\`, and is neither POSIX-absolute, drive-qualified, nor UNC;
- contains no empty, `.`, or `..` component, control character, or NUL;
- has no component with leading/trailing whitespace or a trailing dot;
- contains no `:` and no Windows reserved device component (`CON`, `PRN`,
  `AUX`, `NUL`, `COM1`-`COM9`, or `LPT1`-`LPT9`, including names with an
  extension).

The collision key is `unicodedata.normalize("NFC", path).casefold()`. Each path
list and operation list must have unique collision keys. `allowed_paths` and
`forbidden_paths` must not contain equal or ancestor/descendant collision keys
across the two sets. Every requested operation path must match exactly one
`task.allowed_paths` collision key and must not collide with another operation.
These checks protect portability only; they do not enable filesystem access.

## Baseline and check bindings

`baseline_binding` is a non-empty opaque identifier and is compared byte for
byte. Runtime code does not resolve a branch, commit, filesystem state, or
external service from it.

`task.required_checks` contains unique non-empty names. Evidence check names are
also unique and must exactly cover the required names. Evidence may include
additional checks, but duplicate or collision-prone names are rejected. A
required missing check is `BLOCKED`, never PASS.

## Status precedence

When multiple technical states apply, the runtime reports the first state in
this fail-closed order:

```text
UNKNOWN_BLOCKED > BLOCKED > FAIL > NOT_RUN > HUMAN_REVIEW_REQUIRED > PASS
```

Schema or semantic invalidity is reported separately as `FAIL` and prevents
status aggregation. `PASS` is emitted only when every required check is exactly
`PASS`, all required bindings are current and exact, and unknowns, not-run
items, and blockers are empty. A resulting PASS still maps to
`CONTROL_HUMAN_REVIEW_REQUIRED`, not approval.

## Command exits

| Exit | Meaning |
|---:|---|
| `0` | structurally and semantically valid read-only result; any human review remains separate |
| `2` | command-line usage error produced by `argparse` |
| `3` | malformed YAML/bundle, schema failure, semantic failure, or ordinary blocked control result |
| `4` | execution inputs are structurally and semantically valid, but trusted execution authority or the mutating executor is unavailable |
| `5` | unexpected internal failure, emitted as a fail-closed JSON result |

Exit `4` is limited to `validate-execution`, `preview-execution`, and
`execute-scoped`. Malformed or semantically invalid execution inputs return `3`,
not `4`. No exit code grants approval, execution, Git, merge, or release
authority.

## Explicit limitations

- Trusted human identity and authority verification are not implemented.
- A mutating executor, persistence, transaction recovery, and rollback are not
  implemented.
- Git, network, push, merge, and release actions are not implemented.
- Runtime path checks do not dereference or inspect filesystem paths.
- Runtime schemas are compatibility contracts for version `2.0`; v1 remains a
  historical contract and is not accepted by the v2 loader.
