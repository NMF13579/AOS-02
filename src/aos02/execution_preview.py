"""Non-mutating scoped execution previews."""

from __future__ import annotations

from typing import Any

from .execution_decision import validate_human_execution_decision


def _is_portable_repository_path(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and not value.startswith("/")
        and "\\" not in value
        and "\x00" not in value
        and all(segment not in {"", ".", ".."} for segment in value.split("/"))
    )


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
    if request.get("baseline_binding") != task.get("baseline_binding"):
        reasons.append("REQUEST_BASELINE_BINDING_MISMATCH")
    operations = request.get("operations")
    if not isinstance(operations, list) or not operations:
        reasons.append("OPERATIONS_REQUIRED")
        operations = []
    allowed = set(task.get("allowed_paths", []))
    if any(not isinstance(item, dict) or item.get("path") not in allowed for item in operations):
        reasons.append("OPERATION_OUTSIDE_SCOPE")
    if any(not isinstance(item, dict) or not _is_portable_repository_path(item.get("path")) for item in operations):
        reasons.append("NONPORTABLE_OPERATION_PATH")
    if not validation["local_execution_authorized"]:
        reasons.append("LOCAL_EXECUTION_NOT_AUTHORIZED")
    if reasons:
        return {
            "record_type": "EXECUTION_PREVIEW",
            "schema_version": "2.0",
            "task_binding": task.get("task_id"),
            "baseline_binding": task.get("baseline_binding"),
            "state": "PREVIEW_BLOCKED",
            "execution_readiness": "BLOCKED",
            "reason_codes": sorted(set(reasons)),
            "will_modify_files": False,
            "operation_count": len(operations),
            "operations": [{"action": item.get("action"), "path": item.get("path")} for item in operations if isinstance(item, dict)],
        }
    return {
        "record_type": "EXECUTION_PREVIEW",
        "schema_version": "2.0",
        "task_binding": task.get("task_id"),
        "baseline_binding": task.get("baseline_binding"),
        "state": "PREVIEW_READY",
        "reason_codes": [],
        "will_modify_files": False,
        "operation_count": len(operations),
        "operations": [{"action": item.get("action"), "path": item.get("path")} for item in operations],
    }
