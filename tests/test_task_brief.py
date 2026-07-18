import pytest

from aos02.task_brief import TaskBriefError, compile_task_brief


def test_compile_task_brief_creates_draft_without_human_or_execution_authority():
    task = compile_task_brief(
        idea={"record_type": "IDEA_RECORD", "idea_id": "IDEA-1", "unknowns": []},
        risk={"record_type": "RISK_PROFILE", "risk_id": "RISK-1", "idea_binding": "IDEA-1", "selected_level": "LOW_RISK_DOCUMENTATION_ONLY"},
        scope={"record_type": "SCOPE_AND_CHANGE", "scope_id": "SCOPE-1", "idea_binding": "IDEA-1", "allowed_paths": ["docs/example.md"], "forbidden_paths": ["src/"]},
        task_id="TASK-1",
        required_checks=["markdown"],
    )

    assert task["record_type"] == "TASK_BRIEF"
    assert task["status"] == "DRAFT"
    assert task["idea_binding"] == "IDEA-1"
    assert task["risk_binding"] == "RISK-1"
    assert task["scope_binding"] == "SCOPE-1"
    assert task["required_checks"] == ["markdown"]
    assert task["human_decision_required"] is True
    assert task["execution_authorized"] is False
    assert task["commit_authorized"] is False
    assert task["push_authorized"] is False


def test_compile_task_brief_rejects_unknown_scope():
    with pytest.raises(TaskBriefError, match="UNKNOWN"):
        compile_task_brief(
            idea={"idea_id": "IDEA-1", "unknowns": []},
            risk={"risk_id": "RISK-1", "idea_binding": "IDEA-1"},
            scope={"scope_id": "SCOPE-1", "idea_binding": "IDEA-1", "allowed_paths": ["UNKNOWN"]},
            task_id="TASK-1",
            required_checks=["markdown"],
        )
