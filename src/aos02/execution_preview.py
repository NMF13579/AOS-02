"""Non-mutating scoped execution previews."""

from __future__ import annotations

from typing import Any

from .execution_decision import validate_human_execution_decision


def preview_scoped_execution(
    *, task: dict[str, Any], decision: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Produce a deterministic execution preview; this function never writes files."""
    validation = validate_human_execution_decision(task=task, decision=decision)
    reasons = list(validation["reason_codes"])
    if request.get("record_type") != "EXECUTION_REQUEST":
        reasons.append("WRONG_REQUEST_TYPE")
    if request.get("task_binding") != task.get("task_id"):
        reasons.append("REQUEST_TASK_BINDING_MISMATCH")
    operations = request.get("operations")
    if not isinstance(operations, list) or not operations:
        reasons.append("OPERATIONS_REQUIRED")
        operations = []
    allowed = set(task.get("allowed_paths", []))
    if any(not isinstance(item, dict) or item.get("path") not in allowed for item in operations):
        reasons.append("OPERATION_OUTSIDE_SCOPE")
    if not validation["local_execution_authorized"]:
        reasons.append("LOCAL_EXECUTION_NOT_AUTHORIZED")
    if reasons:
        return {"state": "PREVIEW_BLOCKED", "reason_codes": sorted(set(reasons)), "will_modify_files": False, "operation_count": 0}
    return {
        "state": "PREVIEW_READY",
        "reason_codes": [],
        "will_modify_files": False,
        "operation_count": len(operations),
        "operations": [{"action": item.get("action"), "path": item.get("path")} for item in operations],
    }
