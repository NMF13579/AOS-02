from aos02.execution_preview import preview_scoped_execution


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


def test_preview_returns_non_mutating_plan_for_authorized_scope():
    result = preview_scoped_execution(
        task=task(),
        decision=decision(),
        request={"record_type": "EXECUTION_REQUEST", "task_binding": "TASK-1", "operations": [{"action": "WRITE", "path": "docs/example.md"}]},
    )

    assert result["state"] == "PREVIEW_READY"
    assert result["will_modify_files"] is False
    assert result["operation_count"] == 1


def test_preview_blocks_request_outside_authorized_scope():
    result = preview_scoped_execution(
        task=task(),
        decision=decision(),
        request={"record_type": "EXECUTION_REQUEST", "task_binding": "TASK-1", "operations": [{"action": "WRITE", "path": "src/main.py"}]},
    )

    assert result["state"] == "PREVIEW_BLOCKED"
    assert "OPERATION_OUTSIDE_SCOPE" in result["reason_codes"]
