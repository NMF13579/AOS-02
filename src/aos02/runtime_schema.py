"""Compatibility exports for runtime schema validation."""

from .infrastructure.schema_registry import (
    SCHEMA_FILENAMES,
    SCHEMA_ROOT,
    SchemaValidationError,
    validate_record_schema,
)

__all__ = [
    "SCHEMA_FILENAMES",
    "SCHEMA_ROOT",
    "SchemaValidationError",
    "validate_record_schema",
]
