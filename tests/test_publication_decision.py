from aos02.publication_decision import validate_human_publication_decision


def test_human_publication_decision_records_intent_but_not_git_authority():
    result = validate_human_publication_decision(
        task={"task_id": "TASK-1"},
        evidence={"evidence_id": "EVIDENCE-1"},
        decision={
            "record_type": "HUMAN_PUBLICATION_DECISION",
            "decision_value": "AUTHORIZE_PUBLICATION",
            "task_binding": "TASK-1",
            "evidence_binding": "EVIDENCE-1",
            "decided_by": "HUMAN_OWNER",
        },
    )

    assert result["valid"] is True
    assert result["publication_decision_recorded"] is True
    assert result["commit_authorized"] is False
    assert result["push_authorized"] is False


def test_publication_decision_rejects_implicit_git_authority():
    result = validate_human_publication_decision(
        task={"task_id": "TASK-1"},
        evidence={"evidence_id": "EVIDENCE-1"},
        decision={
            "record_type": "HUMAN_PUBLICATION_DECISION",
            "decision_value": "AUTHORIZE_PUBLICATION",
            "task_binding": "TASK-1",
            "evidence_binding": "EVIDENCE-1",
            "decided_by": "HUMAN_OWNER",
            "push_authorized": True,
        },
    )

    assert result["valid"] is False
    assert "FORBIDDEN_GIT_AUTHORITY_CLAIM" in result["reason_codes"]
