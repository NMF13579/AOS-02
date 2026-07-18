"""R5 documentation package remains owner-readable and explicitly non-authoritative."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[1]
R5_DOCUMENTS = (
    "docs/workflows/owner-control-loop-v1.md",
    "docs/examples/rebuild-v1-fictional-example.md",
    "docs/reviews/rebuild-v1-documentation-dogfood.md",
    "docs/reviews/rebuild-v1-human-review-checklist.md",
)


def test_r5_owner_documentation_package_is_present_and_fail_closed() -> None:
    contents = []
    for relative_path in R5_DOCUMENTS:
        content = (REPOSITORY / relative_path).read_text(encoding="utf-8")
        assert "execution_authorized: false" in content
        assert "mutating_executor: DISABLED" in content
        contents.append(content)

    assert "documentation-only" in contents[2]
    assert "ACCEPT_REBUILD_V1_CANDIDATE" in contents[3]
