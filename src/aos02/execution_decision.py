"""Fail-closed validation of a Human Execution Decision."""

from __future__ import annotations

from typing import Any


FORBIDDEN_GIT_FIELDS = {"commit_authorized", "push_authorized", "merge_authorized", "release_authorized"}


def validate_human_execution_decision(*, task: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded local-execution grant without performing any action."""
    reasons: list[str] = []
    if decision.get("record_type") != "HUMAN_EXECUTION_DECISION":
        reasons.append("WRONG_DECISION_TYPE")
    if decision.get("decided_by") != "HUMAN_OWNER":
        reasons.append("HUMAN_DECIDER_REQUIRED")
    if decision.get("task_binding") != task.get("task_id"):
        reasons.append("TASK_BINDING_MISMATCH")
    if decision.get("allowed_paths") != task.get("allowed_paths"):
        reasons.append("EXECUTION_SCOPE_MISMATCH")
    if any(decision.get(field) is True for field in FORBIDDEN_GIT_FIELDS):
        reasons.append("FORBIDDEN_GIT_AUTHORITY_CLAIM")
    if not reasons and decision.get("decision_value") not in {"ALLOW_LOCAL_EXECUTION", "DENY", "NEEDS_CHANGES"}:
        reasons.append("UNKNOWN_DECISION_VALUE")

    structural_status = "PASS" if not reasons else "FAIL"
    authority_status = "UNTRUSTED"
    if structural_status == "PASS":
        reasons.extend(
            [
                "LOCAL_DECLARED_HUMAN_REFERENCE_NOT_TRUSTED",
                "TRUSTED_HUMAN_AUTHORITY_NOT_IMPLEMENTED",
            ]
        )
    return {
        "valid": structural_status == "PASS",
        "structural_validation": {"status": structural_status},
        "authority_validation": {"status": authority_status},
        "control": {"state": "CONTROL_BLOCKED"},
        "local_execution_authorized": False,
        "execution_authorized": False,
        "reason_codes": reasons,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }
