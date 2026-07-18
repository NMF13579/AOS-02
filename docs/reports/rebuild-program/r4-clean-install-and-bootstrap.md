# R4 — Clean Installation and Developer Bootstrap

```yaml
stage: R4
status: COMPLETE_NON_HERMETIC
fresh_environment: /tmp/aos02-r4-clean
interpreter: Python 3.11
installation: pip install ".[test]"
network_policy: dependency resolution used local pip cache; hermetic wheelhouse absent
installed_package_import: PASS
packaged_runtime_schemas: PASS
CLI_validate_example: PASS
full_test_suite: PASS
full_test_count: 83
runtime_mutation: false
trusted_authority: NOT_IMPLEMENTED
next_required_action: R5_DOCUMENTATION_CONTRACT_ALIGNMENT
```

## Verified path

```bash
python3.11 -m venv /tmp/aos02-r4-clean
/tmp/aos02-r4-clean/bin/python -m pip install ".[test]"
/tmp/aos02-r4-clean/bin/python -m aos02 validate examples/first-bundle
/tmp/aos02-r4-clean/bin/python -m pytest -q
```

The installed package imported from its fresh virtual environment and located its embedded `aos02/schema_data` resources. `validate` produced a technical `PASS` with `CONTROL_HUMAN_REVIEW_REQUIRED`; it did not grant approval or execution authority. The full suite completed with **83 passed**.

## Limitation

This is a clean developer bootstrap validation, not hermetic reproducibility evidence. Dependencies came from the local pip cache and no approved wheelhouse/manifest/hash set exists yet. No claim of offline or network-independent reproducibility is made.
