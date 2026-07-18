from pathlib import Path


def test_runtime_documentation_has_the_verified_clean_environment_command_path():
    repository = Path(__file__).parents[1]
    readme = (repository / "README.md").read_text(encoding="utf-8")
    runtime_guide = (repository / "docs/runtime/executable-control-core.md").read_text(encoding="utf-8")

    assert "documentation only" not in readme.lower()
    assert '.venv/bin/pip install ".[test]"' in runtime_guide
    assert ".venv/bin/python -m pytest" in runtime_guide
    assert "non-mutating control core" in runtime_guide.lower()
    assert "MUTATING_EXECUTOR_DISABLED" in runtime_guide
    assert "mkdir -p /tmp/aos02-example-sandbox" not in runtime_guide
    for command in (
        "validate examples/first-bundle",
        "compile-task examples/first-bundle",
        "validate-execution examples/first-bundle",
        "preview-execution examples/first-bundle",
        "execute-scoped examples/first-bundle --root /tmp/aos02-example-sandbox",
        "validate-result examples/first-bundle",
    ):
        assert command in runtime_guide


def test_v0_closeout_checklist_requires_a_human_decision_separate_from_technical_pass():
    repository = Path(__file__).parents[1]
    checklist = (
        repository / "docs" / "reviews" / "v0-closeout-human-review-checklist.md"
    ).read_text(encoding="utf-8")

    assert "REQUIRES_HUMAN_COMPLETION" in checklist
    assert "Technical PASS is not human approval" in checklist
    assert "ACCEPT_V0_CLOSEOUT" in checklist
    assert "NEEDS_CHANGES_TO_V0_CLOSEOUT" in checklist
    assert "REJECT_V0_CLOSEOUT" in checklist
