# AOS-02 Reference-Driven Rebuild Program Plan

```yaml
plan_id: AOS02-REBUILD-V1
status: DRAFT_FOR_IMPLEMENTATION
project: NMF13579/AOS-02
target_branch: rebuild/aos02-reference-driven-v1
planning_baseline:
  commit: dc8fcd33358ab1c7cb7d340569fe2321a27dd8b2
  tree: 4a00a16227b8b163b4108524606bbcef67a0ed42
reference:
  repository: NMF13579/AOS-FARM
  commit: c3b4f04bdaf504eb4e65d49f60bef92084e3aad0
  role: READ_ONLY_FUNCTIONAL_REFERENCE
  authority: NONE
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

## Short verdict

Rebuild AOS-02 as a **clean modular control application**, using AOS-FARM for validated workflow ideas and safety patterns, but not copying its 500-file `aos/` tree or treating its internal project-control documents as AOS-02 authority.

The current AOS-02 non-mutating v0 is preserved as a tested reference baseline. The rebuild proceeds on `rebuild/aos02-reference-driven-v1`, one independently validated vertical slice at a time.

## Rebuild objective

AOS-02 must become an understandable product that helps an owner run a controlled path:

```text
Idea → Risk + Scope → Task Brief → technical validation / preview
→ Evidence → Human Review
```

It must make these boundaries visible and enforceable:

```text
PASS ≠ approval
Evidence ≠ approval
UNKNOWN / NOT_RUN ≠ PASS
Task Brief ≠ execution authorization
commit ≠ push ≠ merge ≠ release
```

## Target architecture

| Layer | Responsibility | Must not do |
|---|---|---|
| `domain` | Record types, invariant vocabulary, statuses and reason codes | File I/O, CLI, Git, human approval simulation |
| `application` | Use cases: validate, compile draft, preview, create evidence package | Direct filesystem mutation outside explicit adapters |
| `infrastructure` | Strict YAML, JSON Schema, filesystem inspection, Git read adapter | Decide authority or silently widen scope |
| `interfaces/cli` | Parse command input, render structured output, return exit codes | Contain business/control logic |
| `docs` | Product explanation, workflows, examples, reports and review material | Become a second runtime source of truth |
| `tests` | Unit, contract, integration and negative safety matrix | Depend on network or real human authority |

### Runtime topology

Start as a **modular monolith**: one Python package, deterministic local storage, read-only Git inspection, and a CLI. No UI, cloud database, RAG, external identity service, background worker, mutating executor, Git write adapter, merge, or release automation in the first rebuild line.

## Preserve / replace / avoid

| Decision | AOS-FARM reference value | AOS-02 rebuild action |
|---|---|---|
| Preserve | Minimal Safety Floor and explicit human boundary | Keep as AOS-02 product invariants and test them |
| Preserve | Documentation pipeline before code pipeline | Keep as primary user workflow |
| Preserve | Project-local reports and evidence separation | Keep `docs/reports/`, `docs/reviews/`, `docs/examples/` roles separate |
| Preserve | Contract-first, negative-case validation | Keep v2 schema and fail-closed approach where compatible |
| Replace | Large mixed reference layout and internal AOS-FARM project-control hierarchy | Use a small AOS-02-specific package and documentation structure |
| Replace | AOS-FARM-specific `/aos/` consumer kit and registries | Build only adapters/features required by AOS-02 workflows |
| Avoid | Copying reference source/code wholesale | Reimplement behavior from audited requirements and tests |
| Avoid | Approval simulation, hidden lifecycle mutation, auto-merge/release | Keep blocked/unimplemented until a separate architecture plan |

## Stage sequence

### R0 — Reference audit and rebuild plan

```yaml
status: COMPLETE
output:
  - docs/reports/rebuild-program/reference-audit.md
  - docs/reports/rebuild-program/aos02-reference-driven-rebuild-plan.md
validation:
  - reference_commit_recorded
  - preserve_replace_avoid_decision_recorded
  - no_AOS-FARM_files_copied
```

### R1 — Target contract consolidation

Goal: identify one canonical AOS-02 contract map and a precise v1 boundary without rewriting the validated v0 runtime by accident.

Outputs:

```text
- contract-to-domain mapping
- status/reason-code vocabulary
- compatibility decision for existing v2 records
- explicit legacy policy
- migration test fixtures
```

Hard boundary: no authority model weakening; no executor or Git write adapter.

### R2 — Clean package skeleton and deterministic core

Goal: establish the target module boundaries while preserving a working, testable non-mutating vertical slice.

```text
src/aos02/domain/
src/aos02/application/
src/aos02/infrastructure/
src/aos02/interfaces/
```

The first slice is:

```text
load strict record → validate schema + semantics → render structured result
```

No preview/execution mutation in this stage.

### R3 — Scoped workflow vertical slice

Goal: support a full local draft workflow:

```text
Idea + Risk + Scope → Draft Task Brief → read-only validation → Evidence draft
```

Required behavior:

- exact scope narrowing;
- exact baseline binding;
- unknown and missing information block;
- local declared human reference remains untrusted;
- draft output grants no execution/Git authority.

### R4 — CLI and developer bootstrap

Goal: make the supported invocation real and testable in a fresh declared environment.

Required behavior:

- documented install/bootstrap path works;
- command-specific exit codes remain fail-closed;
- package is importable in CLI subprocess tests;
- no hidden `PYTHONPATH` requirement.

### R5 — Documentation and dogfood package

Goal: publish a concise owner workflow, one fictional example, one real documentation-only dogfood task, and project-local evidence/review material.

No UI or external integration is included.

### R6 — Rebuild review and cutover decision

Goal: compare the rebuilt candidate against the v0 baseline and decide whether it may replace the active implementation line.

Required evidence:

- full test matrix;
- clean bootstrap result;
- compatibility/migration result;
- known limitations;
- no mutation/Git-authority regression;
- human review package.

Cutover, merge, and release remain separate human decisions.

## Validation strategy

| Layer | Required checks |
|---|---|
| Domain | Unit tests for statuses, invariant precedence and reason codes |
| Parser/schema | Duplicate-key, alias, tag, type, unknown-field and resource-limit negatives |
| Application | Cross-record binding, scope narrowing, baseline staleness, authority separation |
| CLI | Every command's JSON/status/exit code, including internal error paths |
| Bootstrap | Clean isolated installation and subprocess CLI invocation |
| Documentation | Relative links, examples, no-authority declarations and reports navigation |
| Rebuild acceptance | Full matrix against exact candidate commit/tree |

## Global stop conditions

Stop and produce a project-local report if any of these occur:

- source/reference requirement conflicts with accepted AOS-02 contract;
- a stage needs an unplanned destructive migration or Git history rewrite;
- a proposed feature requires trusted authority, execution mutation, Git write, merge or release;
- the supported bootstrap cannot be made reproducible within its exact stage;
- a record/CLI path can turn `UNKNOWN`, missing data, `NOT_RUN`, or an untrusted local decision into PASS/authority;
- scope requires copying AOS-FARM files rather than reimplementation;
- validation cannot bind to an exact candidate commit/tree.

## Explicit non-goals for rebuild v1

```yaml
trusted_identity_provider: NOT_INCLUDED
cryptographic_approvals: NOT_INCLUDED
mutating_executor: NOT_INCLUDED
transaction_recovery: NOT_INCLUDED
Git_write_adapter: NOT_INCLUDED
merge_or_release_automation: NOT_INCLUDED
UI_or_workbench: NOT_INCLUDED
RAG_or_Supabase: NOT_INCLUDED
multi_agent_runtime: NOT_INCLUDED
```

## First executable work after this plan

**R1: Target contract consolidation.** It begins with a read-only mapping of existing AOS-02 contracts/schemas/tests to the target domain modules, then creates only the mapping, migration fixtures, and tests required to establish the target boundary. It does not restructure runtime code until that mapping is committed and validated.
