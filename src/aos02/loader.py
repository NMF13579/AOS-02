"""Compatibility adapter for strict canonical YAML bundle loading.

The transitional module preserves the public constants used by existing tests while
all new application interfaces depend on ``infrastructure.strict_yaml`` directly.
"""

from pathlib import Path
from typing import Any

from .infrastructure import strict_yaml as _strict_yaml

BundleLoadError = _strict_yaml.BundleLoadError
KNOWN_RECORD_FILENAMES = _strict_yaml.KNOWN_RECORD_FILENAMES
MAX_DOCUMENT_BYTES = _strict_yaml.MAX_DOCUMENT_BYTES
MAX_NESTING_DEPTH = _strict_yaml.MAX_NESTING_DEPTH
MAX_COLLECTION_ITEMS = _strict_yaml.MAX_COLLECTION_ITEMS


def load_records(directory: Path, required_records: tuple[str, ...]) -> dict[str, Any]:
    """Delegate to the target adapter while retaining legacy tunable constants."""
    _strict_yaml.MAX_DOCUMENT_BYTES = MAX_DOCUMENT_BYTES
    _strict_yaml.MAX_NESTING_DEPTH = MAX_NESTING_DEPTH
    _strict_yaml.MAX_COLLECTION_ITEMS = MAX_COLLECTION_ITEMS
    return _strict_yaml.load_records(directory, required_records)


__all__ = [
    "BundleLoadError", "KNOWN_RECORD_FILENAMES", "MAX_COLLECTION_ITEMS",
    "MAX_DOCUMENT_BYTES", "MAX_NESTING_DEPTH", "load_records",
]
