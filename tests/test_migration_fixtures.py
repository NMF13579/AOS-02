"""R1 compatibility fixtures define accepted v2 and rejected legacy input."""

from pathlib import Path

import pytest

from aos02.infrastructure.schema_registry import SchemaValidationError
from aos02.loader import load_records
from aos02.validation import validate_bundle


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "contract-migration"
REQUIRED_RECORDS = ("idea", "risk", "scope", "task", "evidence")


def test_complete_v2_bundle_fixture_remains_technically_valid() -> None:
    result = validate_bundle(load_records(FIXTURE_ROOT / "v2-complete", REQUIRED_RECORDS))

    assert result["validation"]["status"] == "PASS"
    assert result["control"]["state"] == "CONTROL_HUMAN_REVIEW_REQUIRED"


def test_legacy_v1_idea_fixture_is_rejected_without_implicit_migration() -> None:
    with pytest.raises(SchemaValidationError, match="schema validation failed"):
        load_records(FIXTURE_ROOT / "legacy-v1-idea", ("idea",))
