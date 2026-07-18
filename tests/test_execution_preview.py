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
