"""Canonical portable repository path and scope validation."""
from __future__ import annotations

import unicodedata
from typing import Any

WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def is_portable_repository_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value != unicodedata.normalize("NFC", value):
        return False
    if value.startswith("/") or "\\" in value or "\x00" in value or ":" in value:
        return False
    for segment in value.split("/"):
        if not segment or segment in {".", ".."} or segment != segment.strip() or segment.endswith("."):
            return False
        if any(unicodedata.category(character).startswith("C") for character in segment):
            return False
        if segment.split(".", 1)[0].upper() in WINDOWS_RESERVED:
            return False
    return True


def collision_key(path: str) -> str:
    return unicodedata.normalize("NFC", path).casefold()


def same_or_ancestor(parent: str, child: str) -> bool:
    return parent == child or child.startswith(parent + "/")


def validate_task_paths(task: dict[str, Any]) -> list[str]:
    allowed = task.get("allowed_paths", [])
    forbidden = task.get("forbidden_paths", [])
    if not isinstance(allowed, list) or not isinstance(forbidden, list):
        return ["INVALID_SCOPE_PATH_LIST"]
    paths = [*allowed, *forbidden]
    if any(not is_portable_repository_path(path) for path in paths):
        return ["NONPORTABLE_SCOPE_PATH"]
    allowed_keys = [collision_key(path) for path in allowed]
    forbidden_keys = [collision_key(path) for path in forbidden]
    if len(allowed_keys) != len(set(allowed_keys)) or len(forbidden_keys) != len(set(forbidden_keys)):
        return ["PORTABILITY_PATH_COLLISION"]
    if any(same_or_ancestor(left, right) or same_or_ancestor(right, left) for left in allowed_keys for right in forbidden_keys):
        return ["SCOPE_CONFLICT"]
    return []
