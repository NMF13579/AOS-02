from hashlib import sha256
import json

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


def test_executor_preflights_all_operations_before_any_write(tmp_path):
    unsafe_request = request()
    unsafe_request["operations"].append({"action": "DELETE", "path": "docs/example.md"})

    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=unsafe_request)

    assert not (tmp_path / "docs/example.md").exists()
    assert result["checks"][0]["status"] == "NOT_RUN"
    assert result["reason_codes"] == ["UNSUPPORTED_OR_INCOMPLETE_OPERATION"]


def test_executor_persists_pass_evidence_only_inside_sandbox_root(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    evidence_path = tmp_path / ".aos02" / "evidence-report.json"
    assert evidence_path.is_file()
    assert evidence_path.read_text(encoding="utf-8").endswith("\n")
    assert '"record_type": "EVIDENCE_REPORT"' in evidence_path.read_text(encoding="utf-8")
    assert result["evidence_artifact"]["path"] == ".aos02/evidence-report.json"


def test_executor_evidence_artifact_hashes_the_persisted_canonical_report(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    artifact = tmp_path / result["evidence_artifact"]["path"]
    persisted = json.loads(artifact.read_text(encoding="utf-8"))
    assert result["evidence_artifact"]["sha256"] == sha256(artifact.read_bytes()).hexdigest()
    assert persisted == {key: value for key, value in result.items() if key != "evidence_artifact"}
    assert "evidence_artifact" not in persisted


def test_executor_reserves_evidence_artifact_path_from_requested_writes(tmp_path):
    reserved_task = {"task_id": "TASK-1", "allowed_paths": [".aos02/evidence-report.json"]}
    reserved_decision = decision()
    reserved_decision["allowed_paths"] = [".aos02/evidence-report.json"]

    result = execute_scoped_request(
        root=tmp_path,
        task=reserved_task,
        decision=reserved_decision,
        request=request(".aos02/evidence-report.json"),
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["EVIDENCE_ARTIFACT_PATH_RESERVED"]
    persisted = json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))
    assert persisted["status"] == "BLOCKED"
    assert "safe content" not in (tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8")


def test_executor_blocks_non_string_operation_path_with_persisted_evidence(tmp_path):
    malformed_task = {"task_id": "TASK-1", "allowed_paths": [7]}
    malformed_decision = decision()
    malformed_decision["allowed_paths"] = [7]
    malformed_request = request()
    malformed_request["operations"][0]["path"] = 7

    result = execute_scoped_request(
        root=tmp_path,
        task=malformed_task,
        decision=malformed_decision,
        request=malformed_request,
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["INVALID_OPERATION_PATH"]
    assert json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))["status"] == "BLOCKED"


def test_executor_persists_blocked_evidence_inside_explicit_sandbox_root(tmp_path):
    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request("../escape.txt"))

    evidence_path = tmp_path / ".aos02" / "evidence-report.json"
    assert result["status"] == "BLOCKED"
    assert evidence_path.is_file()
    assert json.loads(evidence_path.read_text(encoding="utf-8"))["reason_codes"] == ["OPERATION_OUTSIDE_SCOPE"]
