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
