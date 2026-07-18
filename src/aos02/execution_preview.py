"""Non-mutating scoped execution previews."""

from __future__ import annotations

from typing import Any
import unicodedata

from .execution_decision import validate_human_execution_decision

WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def _is_portable_repository_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value != unicodedata.normalize("NFC", value):
        return False
    if value.startswith("/") or "\\" in value or "\x00" in value or ":" in value:
        return False
    for segment in value.split("/"):
        if not segment or segment in {".", ".."} or segment != segment.strip() or segment.endswith("."):
            return False
        if any(unicodedata.category(character).startswith("C") for character in segment):
            return False
        device_stem = segment.split(".", 1)[0].upper()
        if device_stem in WINDOWS_RESERVED:
            return False
    return True


def _collision_key(path: str) -> str:
    return unicodedata.normalize("NFC", path).casefold()


def _path_is_same_or_ancestor(parent: str, child: str) -> bool:
    return parent == child or child.startswith(parent + "/")


def _has_collision(paths: list[Any]) -> bool:
    keys = [_collision_key(path) for path in paths if isinstance(path, str)]
    return len(keys) != len(paths) or len(keys) != len(set(keys))


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
    allowed_paths = task.get("allowed_paths", [])
    forbidden_paths = task.get("forbidden_paths", [])
    if not isinstance(allowed_paths, list) or not isinstance(forbidden_paths, list):
        reasons.append("INVALID_SCOPE_PATH_LIST")
        allowed_paths, forbidden_paths = [], []
    scope_paths = [*allowed_paths, *forbidden_paths]
    if any(not _is_portable_repository_path(path) for path in scope_paths):
        reasons.append("NONPORTABLE_SCOPE_PATH")
    if _has_collision(allowed_paths) or _has_collision(forbidden_paths) or _has_collision([item.get("path") if isinstance(item, dict) else None for item in operations]):
        reasons.append("PORTABILITY_PATH_COLLISION")
    allowed_keys = {_collision_key(path) for path in allowed_paths if isinstance(path, str)}
    forbidden_keys = [_collision_key(path) for path in forbidden_paths if isinstance(path, str)]
    if any(_path_is_same_or_ancestor(left, right) or _path_is_same_or_ancestor(right, left) for left in allowed_keys for right in forbidden_keys):
        reasons.append("SCOPE_CONFLICT")
    operation_paths = [item.get("path") if isinstance(item, dict) else None for item in operations]
    if any(not _is_portable_repository_path(path) for path in operation_paths):
        reasons.append("NONPORTABLE_OPERATION_PATH")
    operation_keys = [_collision_key(path) for path in operation_paths if isinstance(path, str)]
    if any(key not in allowed_keys for key in operation_keys) or len(operation_keys) != len(operation_paths):
        reasons.append("OPERATION_OUTSIDE_SCOPE")
    if any(any(_path_is_same_or_ancestor(forbidden, key) for forbidden in forbidden_keys) for key in operation_keys):
        reasons.append("OPERATION_IN_FORBIDDEN_SCOPE")
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
