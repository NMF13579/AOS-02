# V0 Clean-Path Technical Evidence

**Status:** `TECHNICAL_OBSERVATION_ONLY`

This record is durable technical evidence for the executable control-core v0 candidate. It is not a Human Decision Record, does not approve the candidate, and grants no authority.

## Verified environment and preconditions

- Repository branch: `build/aos02-executable-control-core`
- Executable source baseline: `d99c307f89db8b46922098a6dc6f478319d91259`
- Environment: local macOS, Python 3.11.15
- Dependency environment: newly created virtual environment at `/tmp/aos02-v0-verify`
- Explicit real-execution sandbox: `/tmp/aos02-v0-sandbox`
- Precondition: `git status --short --branch` reported a clean branch synchronized with `origin/build/aos02-executable-control-core` before the run.

## Observed command path

The runtime guide's documented sequence was exercised with the fresh environment path substituted for `.venv`; all commands below completed with exit code `0`.

```bash
python3.11 -m venv /tmp/aos02-v0-verify
/tmp/aos02-v0-verify/bin/pip install -e ".[test]"
/tmp/aos02-v0-verify/bin/python -m aos02 validate examples/first-bundle
/tmp/aos02-v0-verify/bin/python -m aos02 compile-task examples/first-bundle --task-id EXAMPLE-TASK-DRAFT-002 --check markdown
/tmp/aos02-v0-verify/bin/python -m aos02 validate-execution examples/first-bundle
/tmp/aos02-v0-verify/bin/python -m aos02 preview-execution examples/first-bundle
mkdir -p /tmp/aos02-v0-sandbox
/tmp/aos02-v0-verify/bin/python -m aos02 execute-scoped examples/first-bundle --root /tmp/aos02-v0-sandbox
/tmp/aos02-v0-verify/bin/python -m aos02 validate-result examples/first-bundle
/tmp/aos02-v0-verify/bin/python -m pytest
/tmp/aos02-v0-verify/bin/python -m pip check
git diff --check
```

## Observed results

| Check | Observed result |
|---|---|
| Declared test dependencies | `pip install -e ".[test]"` installed `pytest` and `jsonschema` with the project. |
| Canonical bundle validation | `PASS`; `CONTROL_HUMAN_REVIEW_REQUIRED`; `approval_granted: false`. |
| Draft Task Brief compilation | `DRAFT`; `human_decision_required: true`; no execution or Git authority. |
| Execution-decision validation | valid; local execution only; commit, merge, push, and release remain false. |
| Execution preview | `PREVIEW_READY`; one `WRITE docs/example.md`; `will_modify_files: false`. |
| Scoped execution | `PASS`; wrote only `docs/example.md` plus executor-owned `.aos02/evidence-report.json` below the explicit sandbox. |
| Result-decision validation | valid; commit, merge, push, and release remain false. |
| Runtime schema contracts | included in the full suite with `jsonschema` installed. |
| Full test suite | `64 passed in 0.52s`. |
| Dependency consistency | `No broken requirements found.` |
| Repository whitespace check | `git diff --check` produced no output. |

The scoped execution reported an evidence-artifact SHA-256 of `b68f3e18b665a0db275a19ab8dadb861ecf293e8f5c8b3ba80455140f1b50fc8` for the persisted report and an operation SHA-256 of `5778e10117b6661713f5becec5b4da4391cd93e4016b69c20ae937551e2024e7` for `docs/example.md`.

## Limits

This is a local macOS/Python 3.11 observation of the supplied example bundle and explicit sandbox. It is not hosted-CI evidence; it does not prove arbitrary bundles, operating systems, concurrent writers, external integrations, production behavior, or human approval. In particular, technical `PASS` does not accept a result or authorize a commit, push, merge, release, deployment, or any future scope.
