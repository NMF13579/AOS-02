# AOS-02 Executable Control Core

The first executable component is a **read-only local validator** for canonical YAML bundles. It implements the accepted documentation workflow:

```text
Idea -> Risk + Scope -> Task Brief -> Evidence -> Human Review
```

It validates record bindings, required checks, `UNKNOWN`, `NOT_RUN`, and forbidden approval claims. It does not create decisions, execute changes, touch Git, connect to a network, or grant authority.

## Run locally

```bash
python3.11 -m venv .venv
.venv/bin/pip install . pytest
.venv/bin/python -m aos02 validate examples/first-bundle
.venv/bin/python -m pytest
```

A successful technical result still returns:

```yaml
control:
  state: CONTROL_HUMAN_REVIEW_REQUIRED
approval_granted: false
```

Human review and any execution remain separate, external decisions.
