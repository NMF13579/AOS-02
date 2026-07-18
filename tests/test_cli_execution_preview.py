import json
import subprocess
import sys


def test_cli_generates_non_mutating_execution_preview(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\nallowed_paths: [docs/example.md]\n")
    (tmp_path / "execution-decision.yaml").write_text("record_type: HUMAN_EXECUTION_DECISION\ndecision_value: ALLOW_LOCAL_EXECUTION\ntask_binding: TASK-1\ndecided_by: HUMAN_OWNER\nallowed_paths: [docs/example.md]\n")
    (tmp_path / "execution-request.yaml").write_text("record_type: EXECUTION_REQUEST\ntask_binding: TASK-1\noperations:\n  - action: WRITE\n    path: docs/example.md\n")

    result = subprocess.run([sys.executable, "-m", "aos02", "preview-execution", str(tmp_path)], capture_output=True, text=True, check=False)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["state"] == "PREVIEW_READY"
    assert payload["will_modify_files"] is False
