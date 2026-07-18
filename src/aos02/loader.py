"""Strict closed-world YAML loading for canonical runtime bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from yaml.events import AliasEvent
from yaml.nodes import MappingNode

from .runtime_schema import validate_record_schema

MAX_DOCUMENT_BYTES = 1_048_576
MAX_NESTING_DEPTH = 32
MAX_COLLECTION_ITEMS = 10_000


KNOWN_RECORD_FILENAMES = frozenset(
    {
        "idea.yaml",
        "risk.yaml",
        "scope.yaml",
        "task.yaml",
        "evidence.yaml",
        "execution-decision.yaml",
        "execution-request.yaml",
        "result-decision.yaml",
        "publication-decision.yaml",
    }
)


class BundleLoadError(ValueError):
    """Raised when a bundle is not strict, closed-world canonical YAML."""


class _StrictSafeLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            raise yaml.constructor.ConstructorError(
                None, None, "YAML anchors and aliases are forbidden", self.peek_event().start_mark
            )
        event = self.peek_event()
        if getattr(event, "anchor", None) is not None:
            raise yaml.constructor.ConstructorError(
                None, None, "YAML anchors and aliases are forbidden", event.start_mark
            )
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise yaml.constructor.ConstructorError(
                None, None, "expected a YAML mapping", node.start_mark
            )
        seen: set[str] = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise yaml.constructor.ConstructorError(
                    None, None, "YAML merge keys are forbidden", key_node.start_mark
                )
            key = self.construct_object(key_node, deep=False)
            if not isinstance(key, str):
                raise yaml.constructor.ConstructorError(
                    None, None, "YAML mapping keys must be strings", key_node.start_mark
                )
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate YAML key: {key}", key_node.start_mark
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _load_mapping(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise BundleLoadError(f"document exceeds maximum size: {path.name}")
        data = yaml.load(raw.decode("utf-8"), Loader=_StrictSafeLoader)
    except UnicodeDecodeError as exc:
        raise BundleLoadError(f"invalid UTF-8 in {path.name}") from exc
    except yaml.YAMLError as exc:
        raise BundleLoadError(f"invalid YAML in {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise BundleLoadError(f"record must be a YAML mapping: {path.name}")
    _assert_resource_limits(data)
    return data


def _assert_resource_limits(value: Any, depth: int = 1) -> None:
    if depth > MAX_NESTING_DEPTH:
        raise BundleLoadError("nesting depth exceeds maximum")
    if isinstance(value, dict):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise BundleLoadError("collection exceeds maximum size")
        for child in value.values():
            _assert_resource_limits(child, depth + 1)
    elif isinstance(value, list):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise BundleLoadError("collection exceeds maximum size")
        for child in value:
            _assert_resource_limits(child, depth + 1)


def load_records(directory: Path, required_records: tuple[str, ...]) -> dict[str, Any]:
    """Load all recognized records after enforcing a closed bundle directory."""
    if directory.is_symlink() or not directory.is_dir():
        raise BundleLoadError(f"bundle directory does not exist: {directory}")

    required_filenames = {f"{name}.yaml" for name in required_records}
    unknown_requirements = required_filenames - KNOWN_RECORD_FILENAMES
    if unknown_requirements:
        raise BundleLoadError(
            f"unknown required record: {sorted(unknown_requirements)[0]}"
        )

    entries: dict[str, Path] = {}
    collision_keys: set[str] = set()
    for entry in sorted(directory.iterdir(), key=lambda path: path.name.casefold()):
        if entry.is_symlink() or not entry.is_file():
            raise BundleLoadError(
                f"bundle entry must be a regular non-symlink file: {entry.name}"
            )
        if entry.name not in KNOWN_RECORD_FILENAMES:
            raise BundleLoadError(f"unknown bundle entry: {entry.name}")
        collision_key = entry.name.casefold()
        if collision_key in collision_keys:
            raise BundleLoadError(f"bundle filename collision: {entry.name}")
        collision_keys.add(collision_key)
        entries[entry.name] = entry

    missing = sorted(required_filenames - entries.keys())
    if missing:
        raise BundleLoadError(f"missing canonical record: {missing[0]}")

    records = {
        filename.removesuffix(".yaml"): _load_mapping(path)
        for filename, path in entries.items()
    }
    for name, record in records.items():
        validate_record_schema(name, record)
    return records
