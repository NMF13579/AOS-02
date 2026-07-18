from aos02.result_decision import validate_human_result_decision
from runtime_v2_fixtures import evidence, result_decision, task


def test_valid_human_acceptance_is_bound_to_task_and_evidence_without_git_grant():
    result = validate_human_result_decision(
        task=task(),
        evidence=evidence(),
        decision=result_decision(),
    )

    assert result["valid"] is True
    assert result["result_accepted"] is True
    assert result["commit_authorized"] is False
    assert result["push_authorized"] is False


def test_result_decision_cannot_accept_unrun_evidence():
    report = evidence()
    report["checks"][0]["status"] = "NOT_RUN"

    result = validate_human_result_decision(
        task=task(),
        evidence=report,
        decision=result_decision(),
    )

    assert result["valid"] is False
    assert "EVIDENCE_NOT_PASS" in result["reason_codes"]


def test_result_decision_cannot_accept_blocked_evidence_even_when_checks_pass() -> None:
    report = evidence()
    report["technical_status"] = "BLOCKED"

    result = validate_human_result_decision(
        task=task(), evidence=report, decision=result_decision()
    )

    assert result["valid"] is False
    assert result["result_accepted"] is False
    assert "EVIDENCE_TECHNICAL_STATUS_NOT_PASS" in result["reason_codes"]


def test_result_decision_cannot_accept_evidence_with_remaining_blockers() -> None:
    report = evidence()
    report["blockers"] = ["REMAINING_BLOCKER"]

    result = validate_human_result_decision(
        task=task(), evidence=report, decision=result_decision()
    )

    assert result["valid"] is False
    assert result["result_accepted"] is False
    assert "EVIDENCE_INCOMPLETE" in result["reason_codes"]


def test_result_decision_requires_exact_coverage_of_required_checks() -> None:
    required_task = task()
    required_task["required_checks"] = ["markdown"]
    report = evidence()
    report["checks"] = [{"name": "unrelated", "status": "PASS"}]

    result = validate_human_result_decision(task=required_task, evidence=report, decision=result_decision())

    assert result["valid"] is False
    assert result["result_accepted"] is False
    assert "EVIDENCE_REQUIRED_CHECK_COVERAGE_MISMATCH" in result["reason_codes"]


def test_result_decision_blocks_stale_baseline_binding() -> None:
    stale = result_decision()
    stale["baseline_binding"] = "BASELINE-OTHER"

    result = validate_human_result_decision(task=task(), evidence=evidence(), decision=stale)

    assert result["valid"] is False
    assert result["result_accepted"] is False
    assert "BASELINE_BINDING_MISMATCH" in result["reason_codes"]


def test_result_decision_rejects_implicit_git_authority():
    decision = result_decision()
    decision["push_authorized"] = True

    result = validate_human_result_decision(
        task=task(), evidence=evidence(), decision=decision
    )

    assert result["valid"] is False
    assert "FORBIDDEN_GIT_AUTHORITY_CLAIM" in result["reason_codes"]
