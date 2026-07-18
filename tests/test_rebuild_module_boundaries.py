"""Architecture-boundary regression tests for the R2 modular skeleton."""

from pathlib import Path

import aos02.interfaces.cli as cli
from aos02 import canonical, loader, runtime_schema, validation
from aos02.application import control_validation
from aos02.domain import canonical as domain_canonical
from aos02.infrastructure import schema_registry, strict_yaml


def test_compatibility_modules_delegate_to_target_layers() -> None:
    assert canonical.binding_digest is domain_canonical.binding_digest
    assert loader.load_records is not strict_yaml.load_records
    assert runtime_schema.validate_record_schema is schema_registry.validate_record_schema
    assert validation.validate_bundle is control_validation.validate_bundle


def test_packaged_v2_schemas_match_canonical_repository_schemas() -> None:
    canonical_schema_root = Path(__file__).parents[1] / "schemas" / "runtime"

    for schema_name in schema_registry.SCHEMA_FILENAMES.values():
        assert schema_registry.SCHEMA_ROOT.joinpath(schema_name).read_bytes() == (
            canonical_schema_root / schema_name
        ).read_bytes()


def test_module_entrypoint_delegates_to_cli_interface() -> None:
    assert callable(cli.main)
