"""Isolated, bounded local execution with evidence generation."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
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


def _path_traverses_symlink(*, sandbox: Path, operation_path: str) -> bool:
    """Return whether a requested operation reaches its target through a symlink."""
    current = sandbox
    for component in Path(operation_path).parts:
        current /= component
        if current.is_symlink():
            return True
    return False


def _is_hardlinked_file(target: Path) -> bool:
    """Reject an existing file that could also mutate a location outside the sandbox."""
    return target.is_file() and target.stat().st_nlink > 1


def _evidence_target(*, sandbox: Path) -> Path:
    """Resolve the executor-owned evidence path without permitting symlink indirection."""
    canonical_path = sandbox / _EVIDENCE_ARTIFACT_PATH
    target = canonical_path.resolve()
    if sandbox not in target.parents:
        raise ValueError("evidence artifact escapes explicit sandbox root")
    current = sandbox
    for component in Path(_EVIDENCE_ARTIFACT_PATH).parts:
        current /= component
        if current.is_symlink():
            raise ValueError("evidence artifact path must not traverse a symlink")
    return target


def _persist_evidence(*, sandbox: Path, evidence: dict[str, Any]) -> dict[str, str]:
    """Atomically replace canonical execution evidence in the executor-owned path."""
    target = _evidence_target(sandbox=sandbox)
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(evidence, ensure_ascii=False, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=target.parent, prefix=f".{target.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(serialized)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, target)
    finally:
        temporary_path.unlink(missing_ok=True)
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
    if root.is_symlink():
        raise ValueError("sandbox root must not be a symlink")
    sandbox = root.resolve()
    if sandbox.exists() and not sandbox.is_dir():
        raise ValueError("sandbox root must be a directory")
    evidence_target = _evidence_target(sandbox=sandbox)
    if _is_hardlinked_file(evidence_target):
        raise ValueError("evidence artifact must not be hardlinked")
    if not _target_has_writable_file_path(sandbox=sandbox, target=evidence_target):
        raise ValueError("evidence artifact path is not writable")
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
    if any(target == evidence_target or target in evidence_target.parents or evidence_target in target.parents for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["EVIDENCE_ARTIFACT_PATH_RESERVED"]))
    if any(sandbox not in target.parents for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["SANDBOX_ESCAPE_BLOCKED"]))
    if any(_path_traverses_symlink(sandbox=sandbox, operation_path=operation_path) for operation_path in operation_paths):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["SYMLINK_OPERATION_PATH_BLOCKED"]))
    if any(_is_hardlinked_file(target) for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["HARDLINK_OPERATION_TARGET_BLOCKED"]))
    if any(not _target_has_writable_file_path(sandbox=sandbox, target=target) for target in targets):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["UNWRITABLE_OPERATION_TARGET"]))
    if len(targets) != len(set(targets)):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["DUPLICATE_OPERATION_PATH"]))
    if any(target in other.parents for target in targets for other in targets if target != other):
        return _persist_outcome(sandbox=sandbox, evidence=_blocked_evidence(["OVERLAPPING_OPERATION_PATH"]))

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
