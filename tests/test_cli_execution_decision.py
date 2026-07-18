import json
import subprocess
import sys


def test_cli_validates_bound_execution_decision(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\nallowed_paths: [docs/example.md]\n")
    (tmp_path / "execution-decision.yaml").write_text(
        "record_type: HUMAN_EXECUTION_DECISION\ndecision_value: ALLOW_LOCAL_EXECUTION\ntask_binding: TASK-1\ndecided_by: HUMAN_OWNER\nallowed_paths: [docs/example.md]\n"
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
