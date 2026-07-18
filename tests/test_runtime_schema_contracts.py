import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")


RUNTIME_SCHEMAS = Path(__file__).parents[1] / "schemas" / "runtime"
RUNTIME_FIXTURES = Path(__file__).parent / "fixtures" / "runtime-schema-contracts"


def _validator(schema_name: str):
    schema = json.loads((RUNTIME_SCHEMAS / schema_name).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


@pytest.mark.parametrize(
    ("schema_name", "valid_fixture", "invalid_fixture"),
    [
        (
            "execution-request-1.0.schema.json",
            "valid-execution-request.json",
            "invalid-execution-request-missing-operations.json",
        ),
        (
            "execution-preview-1.0.schema.json",
            "valid-execution-preview-ready.json",
            "invalid-execution-preview-operation-count.json",
        ),
    ],
)
def test_runtime_v1_contracts_validate_focused_fixtures(schema_name, valid_fixture, invalid_fixture):
    validator = _validator(schema_name)
    valid_record = json.loads((RUNTIME_FIXTURES / valid_fixture).read_text(encoding="utf-8"))
    invalid_record = json.loads((RUNTIME_FIXTURES / invalid_fixture).read_text(encoding="utf-8"))

    validator.validate(valid_record)
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(invalid_record)
