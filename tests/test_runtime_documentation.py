from pathlib import Path


def test_runtime_documentation_has_the_verified_clean_environment_command_path():
    repository = Path(__file__).parents[1]
    readme = (repository / "README.md").read_text(encoding="utf-8")
    runtime_guide = (repository / "docs/runtime/executable-control-core.md").read_text(encoding="utf-8")

    assert "documentation only" not in readme.lower()
    assert '.venv/bin/pip install -e ".[test]"' in runtime_guide
    assert ".venv/bin/python -m pytest" in runtime_guide
    for command in (
        "validate examples/first-bundle",
        "compile-task examples/first-bundle",
        "validate-execution examples/first-bundle",
        "preview-execution examples/first-bundle",
        "execute-scoped examples/first-bundle --root /tmp/aos02-example-sandbox",
        "validate-result examples/first-bundle",
    ):
        assert command in runtime_guide
