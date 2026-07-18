from aos02.execution_decision import validate_human_execution_decision


def task():
    return {
        "task_id": "TASK-1",
        "status": "DRAFT",
        "allowed_paths": ["docs/example.md"],
        "forbidden_paths": ["src/"],
    }


def decision():
    return {
        "record_type": "HUMAN_EXECUTION_DECISION",
        "decision_value": "ALLOW_LOCAL_EXECUTION",
        "task_binding": "TASK-1",
        "decided_by": "HUMAN_OWNER",
        "allowed_paths": ["docs/example.md"],
    }


def test_local_human_execution_decision_is_structurally_valid_but_untrusted():
    result = validate_human_execution_decision(task=task(), decision=decision())

    assert result["structural_validation"]["status"] == "PASS"
    assert result["authority_validation"]["status"] == "UNTRUSTED"
    assert result["control"]["state"] == "CONTROL_BLOCKED"
    assert result["local_execution_authorized"] is False
    assert "LOCAL_DECLARED_HUMAN_REFERENCE_NOT_TRUSTED" in result["reason_codes"]
    assert result["commit_authorized"] is False
    assert result["push_authorized"] is False


def test_execution_decision_blocks_scope_expansion():
    expanded = decision()
    expanded["allowed_paths"] = ["docs/example.md", "src/main.py"]

    result = validate_human_execution_decision(task=task(), decision=expanded)

    assert result["valid"] is False
    assert "EXECUTION_SCOPE_MISMATCH" in result["reason_codes"]


def test_execution_decision_rejects_implicit_publication_authority():
    with_git = decision()
    with_git["push_authorized"] = True

    result = validate_human_execution_decision(task=task(), decision=with_git)

    assert result["valid"] is False
    assert "FORBIDDEN_GIT_AUTHORITY_CLAIM" in result["reason_codes"]
