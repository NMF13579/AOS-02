from hashlib import sha256
import json
import os

import pytest

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


def test_executor_rejects_a_non_directory_sandbox_root(tmp_path):
    root = tmp_path / "not-a-directory"
    root.write_text("not a sandbox", encoding="utf-8")

    with pytest.raises(ValueError, match="sandbox root must be a directory"):
        execute_scoped_request(root=root, task=task(), decision=decision(), request=request())


def test_executor_rejects_a_symlinked_sandbox_root_before_writing(tmp_path):
    external_root = tmp_path / "external-root"
    external_root.mkdir()
    root = tmp_path / "sandbox-link"
    root.symlink_to(external_root, target_is_directory=True)

    with pytest.raises(ValueError, match="sandbox root must not be a symlink"):
        execute_scoped_request(root=root, task=task(), decision=decision(), request=request())

    assert not (external_root / "docs/example.md").exists()
    assert not (external_root / ".aos02/evidence-report.json").exists()


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


def test_executor_blocks_duplicate_operation_paths_before_any_write(tmp_path):
    duplicate_request = request()
    duplicate_request["operations"].append(
        {"action": "WRITE", "path": "docs/example.md", "content": "replacement content\n"}
    )

    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=duplicate_request)

    assert not (tmp_path / "docs/example.md").exists()
    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["DUPLICATE_OPERATION_PATH"]
    assert json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))["status"] == "BLOCKED"


def test_executor_blocks_operation_paths_that_resolve_to_the_same_target(tmp_path):
    alias_task = {"task_id": "TASK-1", "allowed_paths": ["docs/example.md", "docs/../docs/example.md"]}
    alias_decision = decision()
    alias_decision["allowed_paths"] = ["docs/example.md", "docs/../docs/example.md"]
    alias_request = request()
    alias_request["operations"].append(
        {"action": "WRITE", "path": "docs/../docs/example.md", "content": "replacement content\n"}
    )

    result = execute_scoped_request(root=tmp_path, task=alias_task, decision=alias_decision, request=alias_request)

    assert not (tmp_path / "docs/example.md").exists()
    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["DUPLICATE_OPERATION_PATH"]


def test_executor_blocks_overlapping_operation_paths_before_any_write(tmp_path):
    parent_path = "docs/generated"
    child_path = "docs/generated/example.md"
    overlapping_task = {"task_id": "TASK-1", "allowed_paths": [parent_path, child_path]}
    overlapping_decision = decision()
    overlapping_decision["allowed_paths"] = [parent_path, child_path]
    overlapping_request = request(parent_path)
    overlapping_request["operations"].append(
        {"action": "WRITE", "path": child_path, "content": "child content\n"}
    )

    result = execute_scoped_request(
        root=tmp_path,
        task=overlapping_task,
        decision=overlapping_decision,
        request=overlapping_request,
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["OVERLAPPING_OPERATION_PATH"]
    assert not (tmp_path / parent_path).exists()
    assert json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))["status"] == "BLOCKED"


def test_executor_rejects_an_internal_symlinked_operation_path(tmp_path):
    symlink_task = {"task_id": "TASK-1", "allowed_paths": ["docs/link.md"]}
    symlink_decision = decision()
    symlink_decision["allowed_paths"] = ["docs/link.md"]
    redirected = tmp_path / "docs" / "redirected.md"
    redirected.parent.mkdir()
    redirected.write_text("original content\n", encoding="utf-8")
    (tmp_path / "docs" / "link.md").symlink_to(redirected)

    result = execute_scoped_request(
        root=tmp_path,
        task=symlink_task,
        decision=symlink_decision,
        request=request("docs/link.md"),
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["SYMLINK_OPERATION_PATH_BLOCKED"]
    assert redirected.read_text(encoding="utf-8") == "original content\n"


def test_executor_rejects_a_hardlinked_operation_target_before_writing(tmp_path):
    external = tmp_path.parent / "external.md"
    external.write_text("original content\n", encoding="utf-8")
    target = tmp_path / "docs" / "example.md"
    target.parent.mkdir()
    os.link(external, target)

    result = execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["HARDLINK_OPERATION_TARGET_BLOCKED"]
    assert external.read_text(encoding="utf-8") == "original content\n"
    assert target.read_text(encoding="utf-8") == "original content\n"


def test_executor_blocks_directory_targets_before_any_write(tmp_path):
    directory_task = {"task_id": "TASK-1", "allowed_paths": ["docs/example.md", "docs/existing-directory"]}
    directory_decision = decision()
    directory_decision["allowed_paths"] = ["docs/example.md", "docs/existing-directory"]
    (tmp_path / "docs/existing-directory").mkdir(parents=True)
    directory_request = request()
    directory_request["operations"].append({"action": "WRITE", "path": "docs/existing-directory", "content": "unsafe\n"})

    result = execute_scoped_request(
        root=tmp_path,
        task=directory_task,
        decision=directory_decision,
        request=directory_request,
    )

    assert not (tmp_path / "docs/example.md").exists()
    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["UNWRITABLE_OPERATION_TARGET"]
    assert json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))["status"] == "BLOCKED"


def test_executor_refuses_an_escaped_evidence_artifact_before_writing_operations(tmp_path):
    outside = tmp_path.parent / "outside-evidence"
    outside.mkdir()
    (tmp_path / ".aos02").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError, match="evidence artifact escapes explicit sandbox root"):
        execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert not (tmp_path / "docs/example.md").exists()
    assert not (outside / "evidence-report.json").exists()


def test_executor_refuses_an_internal_symlink_for_the_canonical_evidence_artifact(tmp_path):
    redirected = tmp_path / "redirected-evidence"
    redirected.mkdir()
    (tmp_path / ".aos02").symlink_to(redirected, target_is_directory=True)

    with pytest.raises(ValueError, match="evidence artifact path must not traverse a symlink"):
        execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert not (tmp_path / "docs/example.md").exists()
    assert not (redirected / "evidence-report.json").exists()


def test_executor_refuses_a_hardlinked_canonical_evidence_artifact(tmp_path):
    external = tmp_path.parent / "external-evidence-report.json"
    external.write_text("original evidence\n", encoding="utf-8")
    artifact = tmp_path / ".aos02" / "evidence-report.json"
    artifact.parent.mkdir()
    os.link(external, artifact)

    with pytest.raises(ValueError, match="evidence artifact must not be hardlinked"):
        execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert not (tmp_path / "docs/example.md").exists()
    assert external.read_text(encoding="utf-8") == "original evidence\n"
    assert artifact.read_text(encoding="utf-8") == "original evidence\n"


def test_executor_refuses_an_unwritable_evidence_artifact_before_writing_operations(tmp_path):
    (tmp_path / ".aos02").write_text("not a directory", encoding="utf-8")

    with pytest.raises(ValueError, match="evidence artifact path is not writable"):
        execute_scoped_request(root=tmp_path, task=task(), decision=decision(), request=request())

    assert not (tmp_path / "docs/example.md").exists()


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


def test_executor_reserves_evidence_artifact_parent_from_requested_writes(tmp_path):
    reserved_task = {"task_id": "TASK-1", "allowed_paths": [".aos02"]}
    reserved_decision = decision()
    reserved_decision["allowed_paths"] = [".aos02"]

    result = execute_scoped_request(
        root=tmp_path,
        task=reserved_task,
        decision=reserved_decision,
        request=request(".aos02"),
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["EVIDENCE_ARTIFACT_PATH_RESERVED"]
    assert (tmp_path / ".aos02").is_dir()
    persisted = json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))
    assert persisted["status"] == "BLOCKED"


def test_executor_reserves_evidence_artifact_descendants_from_requested_writes(tmp_path):
    conflicting_path = ".aos02/evidence-report.json/sidecar"
    reserved_task = {"task_id": "TASK-1", "allowed_paths": [conflicting_path]}
    reserved_decision = decision()
    reserved_decision["allowed_paths"] = [conflicting_path]

    result = execute_scoped_request(
        root=tmp_path,
        task=reserved_task,
        decision=reserved_decision,
        request=request(conflicting_path),
    )

    assert result["status"] == "BLOCKED"
    assert result["reason_codes"] == ["EVIDENCE_ARTIFACT_PATH_RESERVED"]
    assert (tmp_path / ".aos02" / "evidence-report.json").is_file()
    persisted = json.loads((tmp_path / ".aos02/evidence-report.json").read_text(encoding="utf-8"))
    assert persisted["status"] == "BLOCKED"


def test_executor_reserves_evidence_artifact_path_aliases_from_requested_writes(tmp_path):
    reserved_task = {"task_id": "TASK-1", "allowed_paths": [".aos02/../.aos02/evidence-report.json"]}
    reserved_decision = decision()
    reserved_decision["allowed_paths"] = [".aos02/../.aos02/evidence-report.json"]

    result = execute_scoped_request(
        root=tmp_path,
        task=reserved_task,
        decision=reserved_decision,
        request=request(".aos02/../.aos02/evidence-report.json"),
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
