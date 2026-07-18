"""Validation for versioned runtime records emitted by the scoped executor."""

from __future__ import annotations

import re
from typing import Any

EVIDENCE_SCHEMA_VERSION = "1.0"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def validate_runtime_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate the safety-critical subset of the versioned evidence schema.

    The canonical JSON Schema remains the interoperable contract; this dependency-free
    gate keeps runtime emission safe in the control core.
    """
    valid = (
        record.get("record_type") == "EVIDENCE_REPORT"
        and record.get("schema_version") == EVIDENCE_SCHEMA_VERSION
        and record.get("status") in {"PASS", "BLOCKED"}
    )
    if record.get("status") == "PASS":
        artifact = record.get("evidence_artifact")
        artifact_path = artifact.get("path") if isinstance(artifact, dict) else None
        artifact_digest = artifact.get("sha256") if isinstance(artifact, dict) else None
        valid = valid and isinstance(record.get("task_binding"), str) and bool(record["task_binding"])
        valid = valid and isinstance(record.get("operations"), list)
        valid = valid and isinstance(artifact, dict)
        valid = valid and _safe_relative_path(artifact_path) and isinstance(artifact_digest, str) and bool(_SHA256.fullmatch(artifact_digest))
        valid = valid and all(
            isinstance(operation, dict)
            and _safe_relative_path(operation.get("path"))
            and bool(_SHA256.fullmatch(operation.get("sha256", "")))
            for operation in record["operations"]
        )
    return {"valid": bool(valid), "reason_codes": [] if valid else ["SCHEMA_VALIDATION_FAILED"]}
