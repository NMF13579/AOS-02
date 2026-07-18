from aos02.execution import execute_scoped_request


def task():
    return {"task_id": "TASK-1", "allowed_paths": ["docs/example.md"]}


def decision():
    return {
        "record_type": "HUMAN_EXECUTION_DECISION",
        "decision_value": "ALLOW_LOCAL_EXECUTION",
        "task_binding": "TASK-1",
        "decided_by": "HUMAN_OWNER",
        "allowed_paths": ["docs/example.md"],
    }


def request(path="docs/example.md"):
    return {"record_type": "EXECUTION_REQUEST", "task_binding": "TASK-1", "operations": [{"action": "WRITE", "path": path, "content": "safe content\n"}]}


def test_executor_writes_only_authorized_file_under_sandbox_root(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert (tmp_path / "docs/example.md").read_text() == "safe content\n"
    assert result["record_type"] == "EVIDENCE_REPORT"
    assert result["checks"][0]["status"] == "PASS"


def test_executor_blocks_path_traversal_without_writing(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request("../escape.txt"))

    assert not (tmp_path.parent / "escape.txt").exists()
    assert result["checks"][0]["status"] == "NOT_RUN"
    assert "OPERATION_OUTSIDE_SCOPE" in result["reason_codes"]


def test_executor_persists_pass_evidence_only_inside_sandbox_root(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    evidence_path = tmp_path / ".aos02" / "evidence-report.json"
    assert evidence_path.is_file()
    assert evidence_path.read_text(encoding="utf-8").endswith("\n")
    assert '"record_type": "EVIDENCE_REPORT"' in evidence_path.read_text(encoding="utf-8")
    assert result["evidence_artifact"]["path"] == ".aos02/evidence-report.json"
