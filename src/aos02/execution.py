"""Non-mutating execution boundary for AOS-02 control records."""

from __future__ import annotations

from typing import Any

from .execution_preview import preview_scoped_execution
from .runtime_records import EVIDENCE_SCHEMA_VERSION


def _blocked_evidence(reasons: list[str]) -> dict[str, Any]:
    return {
        "record_type": "EVIDENCE_REPORT",
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "status": "BLOCKED",
        "reason_codes": reasons,
        "checks": [{"name": "scoped_execution", "status": "NOT_RUN"}],
        "execution_authorized": False,
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
    return _blocked_evidence(reasons)
