"""Non-runtime structural checks for the fictional manual workflow demonstrator."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = REPOSITORY_ROOT / "docs" / "examples" / "manual-workflow-v0"
README = EXAMPLE_ROOT / "README.md"
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_record(name: str) -> dict[str, Any]:
    return yaml.safe_load((EXAMPLE_ROOT / name).read_text(encoding="utf-8"))


def test_example_chain_is_complete_and_non_authoritative() -> None:
    idea = load_record("idea-record.yaml")
    risk = load_record("risk-profile.yaml")
    scope = load_record("scope-and-change.yaml")
    task = load_record("task-brief.yaml")
    decision = load_record("human-result-decision.yaml")
    evidence = load_record("evidence-report.yaml")

    assert idea["record_type"] == "IDEA_RECORD"
    assert risk["idea_binding"] == idea["idea_id"]
    assert scope["idea_binding"] == idea["idea_id"]
    assert task["idea_binding"] == idea["idea_id"]
    assert task["risk_binding"] == risk["risk_id"]
    assert task["scope_binding"] == scope["scope_id"]
    assert task["status"] == "DRAFT"
    assert task["execution_authorized"] is False
    assert task["commit_authorized"] is False
    assert decision["evidence_binding"] == evidence["evidence_id"]
    assert decision["grants"] == []
    assert {"execution", "commit", "push", "merge", "release"} <= set(decision["non_grants"])
    assert evidence["technical_status"] == "HUMAN_REVIEW_REQUIRED"


def test_example_records_match_runtime_v2_schemas() -> None:
    schema_by_record = {
        "idea-record.yaml": "idea-record-2.0.schema.json",
        "risk-profile.yaml": "risk-profile-2.0.schema.json",
        "scope-and-change.yaml": "scope-and-change-2.0.schema.json",
        "task-brief.yaml": "task-brief-2.0.schema.json",
        "human-result-decision.yaml": "human-result-decision-2.0.schema.json",
        "evidence-report.yaml": "evidence-report-2.0.schema.json",
    }
    schema_root = REPOSITORY_ROOT / "schemas" / "runtime"

    for record_name, schema_name in schema_by_record.items():
        schema = json.loads((schema_root / schema_name).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(load_record(record_name)))
        assert not errors, f"{record_name}: {errors}"


def test_example_readme_links_resolve_and_declare_fictional_boundary() -> None:
    content = README.read_text(encoding="utf-8")

    assert "FICTIONAL_NON_AUTHORITATIVE_DEMONSTRATION" in content
    assert "canonical_authority: NONE" in content
    assert "grants_execution_authorization: false" in content
    for raw_target in LINK_PATTERN.findall(content):
        target = raw_target.split("#", 1)[0]
        assert (README.parent / target).is_file(), target
