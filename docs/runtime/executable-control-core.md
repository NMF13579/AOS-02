# AOS-02 Executable Control Core

The current executable component is a **non-mutating control core** for canonical YAML bundles. It implements the accepted documentation workflow:

```text
Idea -> Risk + Scope -> Task Brief -> Evidence -> Human Review
```

It validates record bindings, required checks, `UNKNOWN`, `NOT_RUN`, and forbidden approval claims. It can compile a **DRAFT-only** Task Brief from Idea/Risk/Scope records. It can validate a local Human Execution Decision structurally and produce a non-mutating preview.

## Safety boundary

Local YAML is not a trusted source of human authority. A structurally valid local record remains:

```yaml
structural_validation:
  status: PASS
authority_validation:
  status: UNTRUSTED
control:
  state: CONTROL_BLOCKED
execution_authorized: false
```

The mutating executor is deliberately disabled. `execute-scoped` returns a blocked Evidence-style result with `MUTATING_EXECUTOR_DISABLED`; it does not create the requested files, directories, `.aos02`, Evidence artifacts, or temporary files.

## Run locally

```bash
python3.11 -m venv .venv
.venv/bin/pip install ".[test]"
.venv/bin/python -m aos02 validate examples/first-bundle
.venv/bin/python -m aos02 compile-task examples/first-bundle --task-id EXAMPLE-TASK-DRAFT-002 --check markdown
.venv/bin/python -m aos02 validate-execution examples/first-bundle  # exits 4: authority untrusted
.venv/bin/python -m aos02 preview-execution examples/first-bundle   # exits 4: readiness blocked
.venv/bin/python -m aos02 execute-scoped examples/first-bundle --root /tmp/aos02-example-sandbox  # exits 4: MUTATING_EXECUTOR_DISABLED
.venv/bin/python -m aos02 validate-result examples/first-bundle
.venv/bin/python -m aos02 validate-publication examples/first-bundle
.venv/bin/python -m pytest
```

A technical PASS is not approval. Human review and any future trusted execution remain separate external decisions.
