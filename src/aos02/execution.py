"""Isolated, bounded local execution with evidence generation."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .execution_preview import preview_scoped_execution
from .runtime_records import EVIDENCE_SCHEMA_VERSION


_EVIDENCE_ARTIFACT_PATH = ".aos02/evidence-report.json"


def _blocked_evidence(reasons: list[str]) -> dict[str, Any]:
    return {
        "record_type": "EVIDENCE_REPORT",
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "status": "BLOCKED",
        "reason_codes": reasons,
        "checks": [{"name": "scoped_execution", "status": "NOT_RUN"}],
    }


def _target_has_writable_file_path(*, sandbox: Path, target: Path) -> bool:
    """Reject existing directories and files that would prevent a complete preflight."""
    if target.exists() and not target.is_file():
        return False
    parent = target.parent
    while parent != sandbox:
        if parent.exists() and not parent.is_dir():
            return False
        parent = parent.parent
    return True


def _persist_evidence(*, sandbox: Path, evidence: dict[str, Any]) -> dict[str, str]:
    """Write canonical execution evidence to the executor-owned workspace path."""
    target = (sandbox / _EVIDENCE_ARTIFACT_PATH).resolve()
    if sandbox not in target.parents:
        raise ValueError("evidence artifact escapes explicit sandbox root")
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(evidence, ensure_ascii=False, sort_keys=True) + "\n"
    target.write_text(serialized, encoding="utf-8")
    return {
        "path": target.relative_to(sandbox).as_posix(),
        "sha256": sha256(target.read_bytes()).hexdigest(),
    }


def _persist_outcome(*, sandbox: Path, evidence: dict[str, Any]) -> dict[str, Any]:
    """Attach a locator after storing the immutable execution outcome in the sandbox."""
    evidence["evidence_artifact"] = _persist_evidence(sandbox=sandbox, evidence=evidence)
    return evidence


def execute_scoped_request(
    *, root: Path, task: dict[str, Any], decision: dict[str, Any], request: dict[str, Any]
) -> dict[str, Any]:
    """Execute allowed WRITE operations strictly below *root* and return Evidence."""
    sandbox = root.resolve()
    if sandbox.exists() and not sandbox.is_dir():
        raise ValueError("sandbox root must be a directory")
    preview = preview_scoped_execution(task=task, decision=decision, request=request)
    if preview["state"] != "PREVIEW_READY":
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(preview["reason_codes"]))

    operations = request["operations"]
    if any(not isinstance(operation.get("path"), str) for operation in operations):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["INVALID_OPERATION_PATH"]))
    if any(operation.get("action") != "WRITE" or not isinstance(operation.get("content"), str) for operation in operations):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["UNSUPPORTED_OR_INCOMPLETE_OPERATION"]))
    operation_paths = [operation["path"] for operation in operations]
    if len(operation_paths) != len(set(operation_paths)):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["DUPLICATE_OPERATION_PATH"]))
    targets = [(sandbox / operation_path).resolve() for operation_path in operation_paths]
    evidence_target = (sandbox / _EVIDENCE_ARTIFACT_PATH).resolve()
    if any(target == evidence_target for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["EVIDENCE_ARTIFACT_PATH_RESERVED"]))
    if any(sandbox not in target.parents for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["SANDBOX_ESCAPE_BLOCKED"]))
    if any(not _target_has_writable_file_path(sandbox=sandbox, target=target) for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["UNWRITABLE_OPERATION_TARGET"]))
    if len(targets) != len(set(targets)):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["DUPLICATE_OPERATION_PATH"]))

    performed: list[dict[str, str]] = []
    for operation, target in zip(operations, targets):
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
    return _persist_outcome(sandbox=sandbox, evidence=evidence)
