"""Fail-closed validation of a separately authored Human Publication Decision."""

from __future__ import annotations

from typing import Any

FORBIDDEN_GIT_FIELDS = {"commit_authorized", "push_authorized", "merge_authorized", "release_authorized"}


def validate_human_publication_decision(
    *, task: dict[str, Any], evidence: dict[str, Any], decision: dict[str, Any]
) -> dict[str, Any]:
    """Record bounded human publication intent; never grant Git authority itself."""
    reasons: list[str] = []
    if decision.get("record_type") != "HUMAN_PUBLICATION_DECISION":
        reasons.append("WRONG_DECISION_TYPE")
    if decision.get("decided_by") != "HUMAN_OWNER":
        reasons.append("HUMAN_DECIDER_REQUIRED")
    if decision.get("task_binding") != task.get("task_id"):
        reasons.append("TASK_BINDING_MISMATCH")
    if decision.get("evidence_binding") != evidence.get("evidence_id"):
        reasons.append("EVIDENCE_BINDING_MISMATCH")
    if any(decision.get(field) is True for field in FORBIDDEN_GIT_FIELDS):
        reasons.append("FORBIDDEN_GIT_AUTHORITY_CLAIM")
    recorded = not reasons and decision.get("decision_value") == "AUTHORIZE_PUBLICATION"
    if not reasons and decision.get("decision_value") not in {"AUTHORIZE_PUBLICATION", "DENY", "NEEDS_CHANGES"}:
        reasons.append("UNKNOWN_DECISION_VALUE")
    return {
        "valid": not reasons,
        "publication_decision_recorded": recorded,
        "reason_codes": reasons,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }
