"""Deterministic preparation of non-authoritative Task Brief drafts."""

from __future__ import annotations

from typing import Any


class TaskBriefError(ValueError):
    """Raised when source records cannot safely produce a task draft."""


def _unknown(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().upper() == "UNKNOWN"
    if isinstance(value, dict):
        return any(_unknown(item) for item in value.values())
    if isinstance(value, list):
        return any(_unknown(item) for item in value)
    return False


def compile_task_brief(
    *,
    idea: dict[str, Any],
    risk: dict[str, Any],
    scope: dict[str, Any],
    task_id: str,
    required_checks: list[str],
) -> dict[str, Any]:
    """Create a DRAFT only; this function never authorizes any operation."""
    idea_id = idea.get("idea_id")
    risk_id = risk.get("risk_id")
    scope_id = scope.get("scope_id")
    if not all(isinstance(value, str) and value for value in (idea_id, risk_id, scope_id, task_id)):
        raise TaskBriefError("idea_id, risk_id, scope_id, and task_id are required")
    if risk.get("idea_binding") != idea_id or scope.get("idea_binding") != idea_id:
        raise TaskBriefError("source record binding mismatch")
    if _unknown(idea.get("unknowns", [])) or _unknown(scope.get("allowed_paths", [])):
        raise TaskBriefError("UNKNOWN source information blocks Task Brief compilation")
    if not required_checks or any(not isinstance(check, str) or not check for check in required_checks):
        raise TaskBriefError("at least one named required check is required")
    return {
        "record_type": "TASK_BRIEF",
        "status": "DRAFT",
        "task_id": task_id,
        "idea_binding": idea_id,
        "risk_binding": risk_id,
        "scope_binding": scope_id,
        "allowed_paths": list(scope.get("allowed_paths", [])),
        "forbidden_paths": list(scope.get("forbidden_paths", [])),
        "required_checks": list(required_checks),
        "human_decision_required": True,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }
