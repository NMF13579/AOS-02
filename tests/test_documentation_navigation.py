"""Non-runtime structural checks for the AOS-02 documentation navigation."""

from __future__ import annotations

import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NAVIGATION_DOCUMENT = REPOSITORY_ROOT / "docs" / "README.md"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def test_documentation_navigation_declares_no_authority() -> None:
    content = NAVIGATION_DOCUMENT.read_text(encoding="utf-8")

    assert "canonical_authority: NONE" in content
    assert "grants_authority: false" in content
    assert "grants_execution_authorization: false" in content
    assert "grants_approval_authority: false" in content


def test_documentation_navigation_local_links_resolve() -> None:
    content = NAVIGATION_DOCUMENT.read_text(encoding="utf-8")
    targets = [target.split("#", 1)[0] for target in MARKDOWN_LINK.findall(content)]

    assert targets
    assert all("://" not in target for target in targets)
    for target in targets:
        assert (NAVIGATION_DOCUMENT.parent / target).is_file(), target
