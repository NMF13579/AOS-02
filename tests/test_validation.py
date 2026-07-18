from aos02.validation import validate_bundle


def valid_bundle():
    return {
        "idea": {"record_type": "IDEA_RECORD", "idea_id": "IDEA-1", "unknowns": []},
        "risk": {"record_type": "RISK_PROFILE", "risk_id": "RISK-1", "idea_binding": "IDEA-1", "selected_level": "LOW_RISK_DOCUMENTATION_ONLY", "decided_by": "HUMAN_OWNER"},
        "scope": {"record_type": "SCOPE_AND_CHANGE", "scope_id": "SCOPE-1", "idea_binding": "IDEA-1", "allowed_paths": ["docs/example.md"], "forbidden_paths": ["src/"]},
        "task": {"record_type": "TASK_BRIEF", "task_id": "TASK-1", "idea_binding": "IDEA-1", "risk_binding": "RISK-1", "scope_binding": "SCOPE-1", "required_checks": ["markdown"]},
        "evidence": {"record_type": "EVIDENCE_REPORT", "task_binding": "TASK-1", "checks": [{"name": "markdown", "status": "PASS"}], "unknowns": [], "not_run": []},
    }


def test_complete_evidence_requires_human_review_not_auto_approval():
    result = validate_bundle(valid_bundle())

    assert result["validation"]["status"] == "PASS"
    assert result["control"]["state"] == "CONTROL_HUMAN_REVIEW_REQUIRED"
    assert result["approval_granted"] is False
    assert result["next_required_action"] == "HUMAN_REVIEW_RESULT"


def test_not_run_required_check_blocks_bundle():
    bundle = valid_bundle()
    bundle["evidence"]["checks"][0]["status"] = "NOT_RUN"

    result = validate_bundle(bundle)

    assert result["validation"]["status"] == "NOT_RUN"
    assert result["control"]["state"] == "CONTROL_BLOCKED"


def test_unknown_required_field_blocks_bundle():
    bundle = valid_bundle()
    bundle["scope"]["allowed_paths"] = ["UNKNOWN"]

    result = validate_bundle(bundle)

    assert result["validation"]["status"] == "UNKNOWN"
    assert result["control"]["state"] == "CONTROL_UNKNOWN_BLOCKED"


def test_false_approval_claim_is_rejected():
    bundle = valid_bundle()
    bundle["evidence"]["approval_granted"] = True

    result = validate_bundle(bundle)

    assert result["validation"]["status"] == "FAIL"
    assert "FORBIDDEN_APPROVAL_CLAIM" in result["reason_codes"]
