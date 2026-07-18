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
