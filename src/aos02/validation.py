"""Fail-closed validation and advisory control-state derivation."""

from __future__ import annotations

from typing import Any

FORBIDDEN_AUTHORITY_FIELDS = {
    "approval_granted",
    "execution_authorized",
    "commit_authorized",
    "push_authorized",
    "merge_authorized",
    "release_authorized",
    "lifecycle_mutated",
}


def _has_forbidden_claim(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_AUTHORITY_FIELDS and child is True:
                return True
            if _has_forbidden_claim(child):
                return True
    if isinstance(value, list):
        return any(_has_forbidden_claim(child) for child in value)
    return False


def _is_unknown(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().upper() == "UNKNOWN"
    if isinstance(value, dict):
        return any(_is_unknown(child) for child in value.values())
    if isinstance(value, list):
        return any(_is_unknown(child) for child in value)
    return False


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate one documentation-control bundle; never create an approval."""
    reasons: list[str] = []
    required = ("idea", "risk", "scope", "task", "evidence")
    missing = [name for name in required if not isinstance(bundle.get(name), dict)]
    if missing:
        reasons.extend(f"MISSING_{name.upper()}" for name in missing)
        return _result("FAIL", "CONTROL_BLOCKED", "FIX_BUNDLE_STRUCTURE", reasons)
    if _has_forbidden_claim(bundle):
        return _result("FAIL", "CONTROL_BLOCKED", "FIX_FORBIDDEN_AUTHORITY_CLAIM", ["FORBIDDEN_APPROVAL_CLAIM"])

    idea, risk, scope, task, evidence = (bundle[name] for name in required)
    if risk.get("idea_binding") != idea.get("idea_id") or scope.get("idea_binding") != idea.get("idea_id"):
        reasons.append("IDEA_BINDING_MISMATCH")
    if task.get("idea_binding") != idea.get("idea_id"):
        reasons.append("TASK_IDEA_BINDING_MISMATCH")
    if task.get("risk_binding") != risk.get("risk_id") or task.get("scope_binding") != scope.get("scope_id"):
        reasons.append("TASK_CONTROL_BINDING_MISMATCH")
    if evidence.get("task_binding") != task.get("task_id"):
        reasons.append("EVIDENCE_TASK_BINDING_MISMATCH")
    if reasons:
        return _result("FAIL", "CONTROL_BLOCKED", "FIX_RECORD_BINDINGS", reasons)

    if _is_unknown(scope.get("allowed_paths")) or _is_unknown(evidence.get("unknowns", [])):
        return _result("UNKNOWN", "CONTROL_UNKNOWN_BLOCKED", "RESOLVE_UNKNOWN", ["UNKNOWN_REQUIRED_INFORMATION"])

    checks = {item.get("name"): item.get("status") for item in evidence.get("checks", []) if isinstance(item, dict)}
    missing_checks = [name for name in task.get("required_checks", []) if name not in checks]
    not_run = [name for name in task.get("required_checks", []) if checks.get(name) == "NOT_RUN"]
    failed = [name for name in task.get("required_checks", []) if checks.get(name) == "FAIL"]
    if missing_checks:
        return _result("FAIL", "CONTROL_BLOCKED", "RUN_REQUIRED_CHECKS", ["MISSING_REQUIRED_CHECK", *missing_checks])
    if not_run:
        return _result("NOT_RUN", "CONTROL_BLOCKED", "RUN_REQUIRED_CHECKS", ["REQUIRED_CHECK_NOT_RUN", *not_run])
    if failed:
        return _result("FAIL", "CONTROL_BLOCKED", "FIX_TECHNICAL_FAILURE", ["REQUIRED_CHECK_FAILED", *failed])
    return _result("PASS", "CONTROL_HUMAN_REVIEW_REQUIRED", "HUMAN_REVIEW_RESULT", [])


def _result(status: str, control_state: str, next_action: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "validation": {"status": status},
        "control": {"state": control_state},
        "reason_codes": reasons,
        "next_required_action": next_action,
        "approval_granted": False,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "lifecycle_mutated": False,
    }
