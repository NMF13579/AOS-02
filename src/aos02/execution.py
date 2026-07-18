"""Non-mutating execution boundary for AOS-02 control records."""

from __future__ import annotations

from typing import Any

from .execution_preview import preview_scoped_execution


def _blocked_outcome(*, task: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "record_type": "EXECUTION_OUTCOME",
        "schema_version": "2.0",
        "task_binding": task.get("task_id"),
        "baseline_binding": task.get("baseline_binding"),
        "technical_status": "BLOCKED",
        "reason_codes": reasons,
        "checks": [{"name": "scoped_execution", "status": "NOT_RUN"}],
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }


def execute_scoped_request(
    *, root: object, task: dict[str, Any], decision: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Return a blocked result without reading from or writing to *root*.

    Trusted human authority and a bounded mutating executor are intentionally not
    implemented. The root is accepted only for CLI/API compatibility and is never
    inspected or used for filesystem access in this control-core profile.
    """
    del root
    preview = preview_scoped_execution(task=task, decision=decision, request=request)
    reasons = sorted(set([*preview.get("reason_codes", []), "MUTATING_EXECUTOR_DISABLED"]))
    return _blocked_outcome(task=task, reasons=reasons)
