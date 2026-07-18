"""Read-only preflight for potential Git publication actions."""

from __future__ import annotations

from typing import Any


def evaluate_git_preflight(
    *,
    publication_decision: dict[str, Any],
    branch: str | None,
    upstream: str | None,
    porcelain_status: str,
    divergence: str | None,
) -> dict[str, Any]:
    """Evaluate factual Git state without invoking or authorizing Git mutation."""
    reasons: list[str] = []
    if not publication_decision.get("valid") or not publication_decision.get("publication_decision_recorded"):
        reasons.append("PUBLICATION_DECISION_REQUIRED")
    if not branch:
        reasons.append("BRANCH_REQUIRED")
    if not upstream:
        reasons.append("UPSTREAM_REQUIRED")
    if porcelain_status.strip():
        reasons.append("WORKTREE_NOT_CLEAN")
    if divergence != "0\t0":
        reasons.append("BRANCH_NOT_SYNCHRONIZED")
    return {
        "state": "GIT_PREFLIGHT_BLOCKED" if reasons else "GIT_PREFLIGHT_READY",
        "reason_codes": reasons,
        "branch": branch,
        "upstream": upstream,
        "git_action_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }
