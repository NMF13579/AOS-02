from aos02.git_preflight import evaluate_git_preflight


def test_git_preflight_requires_recorded_human_publication_intent_and_clean_tracking_branch():
    result = evaluate_git_preflight(
        publication_decision={"valid": True, "publication_decision_recorded": True},
        branch="build/aos02-executable-control-core",
        upstream="origin/build/aos02-executable-control-core",
        porcelain_status="",
        divergence="0\t0",
    )

    assert result["state"] == "GIT_PREFLIGHT_READY"
    assert result["git_action_authorized"] is False


def test_git_preflight_blocks_dirty_or_unapproved_state():
    result = evaluate_git_preflight(
        publication_decision={"valid": False, "publication_decision_recorded": False},
        branch="main",
        upstream=None,
        porcelain_status=" M src/aos02/execution.py",
        divergence=None,
    )

    assert result["state"] == "GIT_PREFLIGHT_BLOCKED"
    assert set(result["reason_codes"]) >= {"PUBLICATION_DECISION_REQUIRED", "WORKTREE_NOT_CLEAN", "UPSTREAM_REQUIRED"}
