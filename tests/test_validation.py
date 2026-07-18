from aos02.validation import validate_bundle
from runtime_v2_fixtures import full_bundle


def valid_bundle():
    records = full_bundle()
    return {name: records[name] for name in ("idea", "risk", "scope", "task", "evidence")}


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
