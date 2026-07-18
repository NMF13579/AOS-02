import json
import subprocess
import sys

import yaml

from runtime_v2_fixtures import execution_decision, task


def test_cli_validates_bound_execution_decision(tmp_path):
    for name, record in {
        "task": task(),
        "execution-decision": execution_decision(),
    }.items():
        (tmp_path / f"{name}.yaml").write_text(
            yaml.safe_dump(record, sort_keys=False), encoding="utf-8"
        )

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "validate-execution", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["structural_validation"]["status"] == "PASS"
    assert payload["authority_validation"]["status"] == "UNTRUSTED"
    assert payload["local_execution_authorized"] is False
    assert payload["push_authorized"] is False


def test_cli_returns_exit_3_for_malformed_execution_input(tmp_path):
    (tmp_path / "task.yaml").write_text("record_type: [\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "validate-execution", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 3
    assert json.loads(result.stdout)["validation"]["status"] == "FAIL"
