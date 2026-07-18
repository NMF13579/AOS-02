from aos02.publication_decision import validate_human_publication_decision
from runtime_v2_fixtures import evidence, publication_decision, task


def test_human_publication_decision_records_intent_but_not_git_authority():
    result = validate_human_publication_decision(
        task=task(), evidence=evidence(), decision=publication_decision()
    )

    assert result["valid"] is True
    assert result["publication_decision_recorded"] is True
    assert result["commit_authorized"] is False
    assert result["push_authorized"] is False


def test_publication_decision_blocks_stale_baseline_binding() -> None:
    stale = publication_decision()
    stale["baseline_binding"] = "BASELINE-OTHER"

    result = validate_human_publication_decision(task=task(), evidence=evidence(), decision=stale)

    assert result["valid"] is False
    assert result["publication_decision_recorded"] is False
    assert "BASELINE_BINDING_MISMATCH" in result["reason_codes"]


def test_publication_decision_rejects_implicit_git_authority():
    decision = publication_decision()
    decision["push_authorized"] = True

    result = validate_human_publication_decision(
        task=task(), evidence=evidence(), decision=decision
    )

    assert result["valid"] is False
    assert "FORBIDDEN_GIT_AUTHORITY_CLAIM" in result["reason_codes"]
