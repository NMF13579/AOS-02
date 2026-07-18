"""Dependency-free validation against AOS-02 runtime JSON Schema v2 files."""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
import json
import re
from typing import Any


SCHEMA_FILENAMES = {
    "idea": "idea-record-2.0.schema.json",
    "risk": "risk-profile-2.0.schema.json",
    "scope": "scope-and-change-2.0.schema.json",
    "task": "task-brief-2.0.schema.json",
    "evidence": "evidence-report-2.0.schema.json",
    "execution-decision": "human-execution-decision-2.0.schema.json",
    "execution-request": "execution-request-2.0.schema.json",
    "result-decision": "human-result-decision-2.0.schema.json",
    "publication-decision": "human-publication-decision-2.0.schema.json",
}
SCHEMA_ROOT = files("aos02").joinpath("schema_data")


class SchemaValidationError(ValueError):
    """Raised when one runtime record does not conform to its v2 schema."""


@lru_cache(maxsize=None)
def _load_schema(schema_name: str) -> dict[str, Any]:
    with SCHEMA_ROOT.joinpath(schema_name).open(encoding="utf-8") as stream:
        schema = json.load(stream)
    if not isinstance(schema, dict):
        raise RuntimeError(f"runtime schema is not an object: {schema_name}")
    return schema


def _matches_type(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }.get(expected, False)


def _validate(value: Any, schema: dict[str, Any], path: str) -> None:
    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(value, expected_type):
        raise SchemaValidationError(f"{path}: expected {expected_type}")
    if "const" in schema and value != schema["const"]:
        raise SchemaValidationError(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise SchemaValidationError(f"{path}: value is outside the closed enum")
    if isinstance(value, dict):
        missing = [name for name in schema.get("required", []) if name not in value]
        if missing:
            raise SchemaValidationError(f"{path}: missing required field {missing[0]}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise SchemaValidationError(f"{path}: unknown field {unknown[0]}")
        for name, child in value.items():
            if name in properties:
                _validate(child, properties[name], f"{path}.{name}")
    if isinstance(value, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(value) < minimum:
            raise SchemaValidationError(f"{path}: expected at least {minimum} items")
        if schema.get("uniqueItems") is True:
            for index, item in enumerate(value):
                if item in value[:index]:
                    raise SchemaValidationError(f"{path}: duplicate array item")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate(item, item_schema, f"{path}[{index}]")
    if isinstance(value, str):
        minimum = schema.get("minLength")
        if minimum is not None and len(value) < minimum:
            raise SchemaValidationError(f"{path}: string is shorter than {minimum}")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            raise SchemaValidationError(f"{path}: string does not match required pattern")
    if isinstance(value, int) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if minimum is not None and value < minimum:
            raise SchemaValidationError(f"{path}: integer is below {minimum}")


def validate_record_schema(record_name: str, record: dict[str, Any]) -> None:
    """Validate one named input record from the closed runtime registry."""
    try:
        schema_name = SCHEMA_FILENAMES[record_name]
    except KeyError as exc:
        raise SchemaValidationError(f"unknown runtime record: {record_name}") from exc
    try:
        _validate(record, _load_schema(schema_name), "$")
    except SchemaValidationError as exc:
        raise SchemaValidationError(
            f"schema validation failed for {record_name}.yaml: {exc}"
        ) from exc
