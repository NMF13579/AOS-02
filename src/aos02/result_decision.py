"""Validation of an externally authored Human Result Decision."""

from __future__ import annotations

from typing import Any


FORBIDDEN_GIT_FIELDS = {"commit_authorized", "push_authorized", "merge_authorized", "release_authorized"}


def validate_human_result_decision(
    *, task: dict[str, Any], evidence: dict[str, Any], decision: dict[str, Any]
) -> dict[str, Any]:
    """Validate an acceptance record; validation itself never grants Git authority."""
    reasons: list[str] = []
    if decision.get("record_type") != "HUMAN_DECISION_RECORD" or decision.get(
        "decision_type"
    ) != "RESULT_ACCEPTANCE":
        reasons.append("WRONG_DECISION_TYPE")
    if decision.get("decided_by") != "HUMAN_OWNER":
        reasons.append("HUMAN_DECIDER_REQUIRED")
    if decision.get("scope_binding") != task.get("task_id"):
        reasons.append("TASK_BINDING_MISMATCH")
    if decision.get("status") != "HUMAN_ACCEPTED":
        reasons.append("DECISION_NOT_HUMAN_ACCEPTED")
    if decision.get("evidence_binding") != evidence.get("evidence_id"):
        reasons.append("EVIDENCE_BINDING_MISMATCH")
    if decision.get("baseline_binding") != task.get("baseline_binding") or evidence.get("baseline_binding") != task.get("baseline_binding"):
        reasons.append("BASELINE_BINDING_MISMATCH")
    if any(decision.get(field) is True for field in FORBIDDEN_GIT_FIELDS):
        reasons.append("FORBIDDEN_GIT_AUTHORITY_CLAIM")
    if evidence.get("technical_status") != "PASS":
        reasons.append("EVIDENCE_TECHNICAL_STATUS_NOT_PASS")
    checks = evidence.get("checks", [])
    if not checks or any(not isinstance(check, dict) or check.get("status") != "PASS" for check in checks):
        reasons.append("EVIDENCE_NOT_PASS")
    if evidence.get("unknowns") or evidence.get("not_run") or evidence.get("blockers"):
        reasons.append("EVIDENCE_INCOMPLETE")
    accepted = not reasons and decision.get("decision_value") == "ACCEPT"
    if not reasons and decision.get("decision_value") not in {"ACCEPT", "NEEDS_CHANGES", "REJECT"}:
        reasons.append("UNKNOWN_DECISION_VALUE")
    return {
        "valid": not reasons,
        "result_accepted": accepted,
        "reason_codes": reasons,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }
