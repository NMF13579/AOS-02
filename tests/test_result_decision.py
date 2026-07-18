from aos02.result_decision import validate_human_result_decision


def evidence():
    return {
        "record_type": "EVIDENCE_REPORT",
        "evidence_id": "EVIDENCE-1",
        "task_binding": "TASK-1",
        "checks": [{"name": "markdown", "status": "PASS"}],
        "unknowns": [],
        "not_run": [],
    }


def test_valid_human_acceptance_is_bound_to_task_and_evidence_without_git_grant():
    result = validate_human_result_decision(
        task={"task_id": "TASK-1"},
        evidence=evidence(),
        decision={
            "record_type": "HUMAN_RESULT_DECISION",
            "decision_value": "ACCEPT",
            "task_binding": "TASK-1",
            "evidence_binding": "EVIDENCE-1",
            "decided_by": "HUMAN_OWNER",
        },
    )

    assert result["valid"] is True
    assert result["result_accepted"] is True
    assert result["commit_authorized"] is False
    assert result["push_authorized"] is False


def test_result_decision_cannot_accept_unrun_evidence():
    report = evidence()
    report["checks"][0]["status"] = "NOT_RUN"

    result = validate_human_result_decision(
        task={"task_id": "TASK-1"},
        evidence=report,
        decision={
            "record_type": "HUMAN_RESULT_DECISION",
            "decision_value": "ACCEPT",
            "task_binding": "TASK-1",
            "evidence_binding": "EVIDENCE-1",
            "decided_by": "HUMAN_OWNER",
        },
    )

    assert result["valid"] is False
    assert "EVIDENCE_NOT_PASS" in result["reason_codes"]


def test_result_decision_rejects_implicit_git_authority():
    result = validate_human_result_decision(
        task={"task_id": "TASK-1"},
        evidence=evidence(),
        decision={
            "record_type": "HUMAN_RESULT_DECISION",
            "decision_value": "ACCEPT",
            "task_binding": "TASK-1",
            "evidence_binding": "EVIDENCE-1",
            "decided_by": "HUMAN_OWNER",
            "push_authorized": True,
        },
    )

    assert result["valid"] is False
    assert "FORBIDDEN_GIT_AUTHORITY_CLAIM" in result["reason_codes"]
