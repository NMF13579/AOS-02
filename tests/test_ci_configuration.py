from pathlib import Path

import yaml


def test_ci_runs_full_pytest_on_supported_python():
    workflow = Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))

    assert config["name"] == "CI"
    assert "push" in config[True]
    assert "pull_request" in config[True]
    steps = config["jobs"]["test"]["steps"]
    assert any(step.get("run") == "python -m pytest -q" for step in steps)


def test_ci_uses_least_privilege_and_pinned_actions():
    workflow = Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))

    job = config["jobs"]["test"]
    assert job["timeout-minutes"] == 10

    steps = job["steps"]
    checkout_step = next(step for step in steps if "actions/checkout@" in step.get("uses", ""))
    setup_python_step = next(
        step for step in steps if "actions/setup-python@" in step.get("uses", "")
    )

    assert checkout_step["uses"].split("@", 1)[1] == "11bd71901bbe5b1630ceea73d27597364c9af683"
    assert checkout_step["with"]["persist-credentials"] is False
    assert setup_python_step["uses"].split("@", 1)[1] == "0a5c61591373683505ea898e09a3ea4f39ef2b9c"
