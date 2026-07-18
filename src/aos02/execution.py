"""Isolated, bounded local execution with evidence generation."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
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
    }


def _persist_evidence(*, sandbox: Path, evidence: dict[str, Any]) -> dict[str, str]:
    """Write canonical execution evidence to the executor-owned workspace path."""
    target = (sandbox / ".aos02" / "evidence-report.json").resolve()
    if sandbox not in target.parents:
        raise ValueError("evidence artifact escapes explicit sandbox root")
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(evidence, ensure_ascii=False, sort_keys=True) + "\n"
    target.write_text(serialized, encoding="utf-8")
    return {
        "path": target.relative_to(sandbox).as_posix(),
        "sha256": sha256(target.read_bytes()).hexdigest(),
    }


def execute_scoped_request(
    *, root: Path, task: dict[str, Any], decision: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Execute allowed WRITE operations strictly below *root* and return Evidence."""
    preview = preview_scoped_execution(task=task, decision=decision, request=request)
    if preview["state"] != "PREVIEW_READY":
        return _blocked_evidence(preview["reason_codes"])

    sandbox = root.resolve()
    operations = request["operations"]
    if any(operation.get("action") != "WRITE" or not isinstance(operation.get("content"), str) for operation in operations):
        return _blocked_evidence(["UNSUPPORTED_OR_INCOMPLETE_OPERATION"])

    performed: list[dict[str, str]] = []
    for operation in operations:
        target = (sandbox / operation["path"]).resolve()
        if sandbox not in target.parents:
            return _blocked_evidence(["SANDBOX_ESCAPE_BLOCKED"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(operation["content"], encoding="utf-8")
        performed.append({"path": operation["path"], "sha256": sha256(target.read_bytes()).hexdigest()})

    evidence = {
        "record_type": "EVIDENCE_REPORT",
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "status": "PASS",
        "task_binding": task["task_id"],
        "reason_codes": [],
        "checks": [{"name": "scoped_execution", "status": "PASS"}],
        "operations": performed,
    }
    evidence["evidence_artifact"] = _persist_evidence(sandbox=sandbox, evidence=evidence)
    return evidence
