import pytest

from aos02.execution_preview import preview_scoped_execution
from runtime_v2_fixtures import execution_decision as decision
from runtime_v2_fixtures import execution_request, task


def test_preview_returns_plan_but_blocks_execution_without_trusted_authority():
    result = preview_scoped_execution(
        task=task(),
        decision=decision(),
        request=execution_request(),
    )

    assert result["state"] == "PREVIEW_BLOCKED"
    assert result["execution_readiness"] == "BLOCKED"
    assert result["will_modify_files"] is False
    assert result["operation_count"] == 1
    assert "LOCAL_DECLARED_HUMAN_REFERENCE_NOT_TRUSTED" in result["reason_codes"]


def test_preview_blocks_request_with_stale_baseline() -> None:
    stale_request = execution_request()
    stale_request["baseline_binding"] = "BASELINE-OTHER"

    result = preview_scoped_execution(task=task(), decision=decision(), request=stale_request)

    assert result["state"] == "PREVIEW_BLOCKED"
    assert "REQUEST_BASELINE_BINDING_MISMATCH" in result["reason_codes"]


def test_preview_blocks_nonportable_path_even_when_task_lists_it_as_allowed() -> None:
    unsafe_task = task()
    unsafe_task["allowed_paths"] = ["../escape"]
    unsafe_request = execution_request()
    unsafe_request["operations"] = [{"action": "WRITE", "path": "../escape", "content": ""}]

    result = preview_scoped_execution(task=unsafe_task, decision=decision(), request=unsafe_request)

    assert result["state"] == "PREVIEW_BLOCKED"
    assert "NONPORTABLE_OPERATION_PATH" in result["reason_codes"]


@pytest.mark.parametrize(
    "unsafe_path",
    ["C:/escape", "CON", "NUL.txt", "docs/name.", "docs/ name ", "docs/\x01name", "docs/e\u0301.md"],
)
def test_preview_blocks_all_nonportable_contract_paths(unsafe_path: str) -> None:
    unsafe_task = task()
    unsafe_task["allowed_paths"] = [unsafe_path]
    unsafe_request = execution_request()
    unsafe_request["operations"] = [{"action": "WRITE", "path": unsafe_path, "content": ""}]

    result = preview_scoped_execution(task=unsafe_task, decision=decision(), request=unsafe_request)

    assert "NONPORTABLE_OPERATION_PATH" in result["reason_codes"]


def test_preview_detects_allowed_path_collision() -> None:
    unsafe_task = task()
    unsafe_task["allowed_paths"] = ["docs/A.md", "docs/a.md"]
    unsafe_task["forbidden_paths"] = []

    result = preview_scoped_execution(task=unsafe_task, decision=decision(), request=execution_request())

    assert "PORTABILITY_PATH_COLLISION" in result["reason_codes"]


def test_preview_matches_allowed_paths_by_collision_key() -> None:
    portable_task = task()
    portable_task["allowed_paths"] = ["Docs/File.md"]
    portable_task["forbidden_paths"] = []
    request = execution_request()
    request["operations"] = [{"action": "WRITE", "path": "docs/file.md", "content": ""}]

    result = preview_scoped_execution(task=portable_task, decision=decision(), request=request)

    assert "OPERATION_OUTSIDE_SCOPE" not in result["reason_codes"]


def test_preview_detects_allowed_forbidden_ancestor_conflict() -> None:
    unsafe_task = task()
    unsafe_task["allowed_paths"] = ["docs/file.md"]
    unsafe_task["forbidden_paths"] = ["DOCS"]

    result = preview_scoped_execution(task=unsafe_task, decision=decision(), request=execution_request())

    assert "SCOPE_CONFLICT" in result["reason_codes"]


def test_preview_blocks_request_outside_authorized_scope():
    result = preview_scoped_execution(
        task=task(),
        decision=decision(),
        request={
            **execution_request(),
            "operations": [{"action": "WRITE", "path": "src/main.py", "content": ""}],
        },
    )

    assert result["state"] == "PREVIEW_BLOCKED"
    assert "OPERATION_OUTSIDE_SCOPE" in result["reason_codes"]
