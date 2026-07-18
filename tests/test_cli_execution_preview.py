import json
import subprocess
import sys


def test_cli_generates_non_mutating_execution_preview(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\nallowed_paths: [docs/example.md]\n")
    (tmp_path / "execution-decision.yaml").write_text("record_type: HUMAN_EXECUTION_DECISION\ndecision_value: ALLOW_LOCAL_EXECUTION\ntask_binding: TASK-1\ndecided_by: HUMAN_OWNER\nallowed_paths: [docs/example.md]\n")
    (tmp_path / "execution-request.yaml").write_text("record_type: EXECUTION_REQUEST\ntask_binding: TASK-1\noperations:\n  - action: WRITE\n    path: docs/example.md\n")

    result = subprocess.run([sys.executable, "-m", "aos02", "preview-execution", str(tmp_path)], capture_output=True, text=True, check=False)

    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["state"] == "PREVIEW_BLOCKED"
    assert payload["execution_readiness"] == "BLOCKED"
    assert payload["will_modify_files"] is False


def test_cli_executes_authorized_request_only_under_explicit_root(tmp_path):
    bundle = tmp_path / "bundle"
    root = tmp_path / "sandbox"
    bundle.mkdir()
    (bundle / "task.yaml").write_text("task_id: TASK-1\nallowed_paths: [docs/example.md]\n")
    (bundle / "execution-decision.yaml").write_text("record_type: HUMAN_EXECUTION_DECISION\ndecision_value: ALLOW_LOCAL_EXECUTION\ntask_binding: TASK-1\ndecided_by: HUMAN_OWNER\nallowed_paths: [docs/example.md]\n")
    (bundle / "execution-request.yaml").write_text("record_type: EXECUTION_REQUEST\ntask_binding: TASK-1\noperations:\n  - action: WRITE\n    path: docs/example.md\n    content: |\n      safe content\n")

    result = subprocess.run([sys.executable, "-m", "aos02", "execute-scoped", str(bundle), "--root", str(root)], capture_output=True, text=True, check=False)

    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["status"] == "BLOCKED"
    assert "MUTATING_EXECUTOR_DISABLED" in payload["reason_codes"]
    assert not root.exists()
    assert not (root / "docs/example.md").exists()
    assert not (root / ".aos02").exists()
