import json
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

from aos02.loader import load_records
from runtime_v2_fixtures import (
    evidence,
    execution_decision,
    execution_outcome,
    execution_preview,
    execution_request,
    idea,
    publication_decision,
    result_decision,
    risk,
    scope,
    task,
)


SCHEMA_ROOT = Path(__file__).parents[1] / "schemas" / "runtime"
SCHEMA_CASES = {
    "idea-record-2.0.schema.json": idea,
    "risk-profile-2.0.schema.json": risk,
    "scope-and-change-2.0.schema.json": scope,
    "task-brief-2.0.schema.json": task,
    "evidence-report-2.0.schema.json": evidence,
    "human-execution-decision-2.0.schema.json": execution_decision,
    "execution-request-2.0.schema.json": execution_request,
    "human-result-decision-2.0.schema.json": result_decision,
    "human-publication-decision-2.0.schema.json": publication_decision,
    "execution-preview-2.0.schema.json": execution_preview,
    "execution-outcome-2.0.schema.json": execution_outcome,
}


def _assert_objects_are_closed(schema):
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            assert schema.get("additionalProperties") is False
        for value in schema.values():
            _assert_objects_are_closed(value)
    elif isinstance(schema, list):
        for value in schema:
            _assert_objects_are_closed(value)


@pytest.mark.parametrize(("schema_name", "record_factory"), SCHEMA_CASES.items())
def test_runtime_v2_schema_is_valid_closed_world_and_rejects_unknown_fields(
    schema_name, record_factory
):
    schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    _assert_objects_are_closed(schema)
    validator = jsonschema.Draft202012Validator(schema)

    validator.validate(record_factory())
    unexpected = record_factory()
    unexpected["unexpected"] = True
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(unexpected)


def _write_bundle(directory, records):
    for name, record in records.items():
        (directory / f"{name}.yaml").write_text(
            yaml.safe_dump(record, sort_keys=False), encoding="utf-8"
        )


def test_production_loader_rejects_unversioned_records(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="schema validation failed"):
        load_records(tmp_path, ("task",))


def test_production_loader_schema_validates_recognized_extra_records(tmp_path):
    request = execution_request()
    request["unexpected"] = True
    _write_bundle(tmp_path, {"task": task(), "execution-request": request})

    with pytest.raises(ValueError, match="execution-request.yaml"):
        load_records(tmp_path, ("task",))


def test_production_schema_resolution_is_independent_of_current_directory(tmp_path, monkeypatch):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    _write_bundle(bundle, {"task": task()})
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    records = load_records(bundle, ("task",))

    assert records["task"] == task()
