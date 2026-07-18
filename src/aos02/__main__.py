"""Read-only CLI adapter for AOS-02 canonical record bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from .validation import validate_bundle

REQUIRED_RECORDS = ("idea", "risk", "scope", "task", "evidence")


def load_bundle(directory: Path) -> dict[str, Any]:
    if not directory.is_dir():
        raise ValueError(f"bundle directory does not exist: {directory}")
    bundle: dict[str, Any] = {}
    for name in REQUIRED_RECORDS:
        path = directory / f"{name}.yaml"
        if not path.is_file():
            raise ValueError(f"missing canonical record: {path.name}")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"record must be a YAML mapping: {path.name}")
        bundle[name] = data
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aos02", description="AOS-02 read-only control validation")
    subcommands = parser.add_subparsers(dest="command", required=True)
    validate = subcommands.add_parser("validate", help="validate a canonical YAML record bundle")
    validate.add_argument("bundle", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_bundle(load_bundle(args.bundle))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        result = {
            "validation": {"status": "FAIL"},
            "control": {"state": "CONTROL_BLOCKED"},
            "reason_codes": ["BUNDLE_LOAD_ERROR", str(exc)],
            "next_required_action": "FIX_BUNDLE_STRUCTURE",
            "approval_granted": False,
            "execution_authorized": False,
            "commit_authorized": False,
            "push_authorized": False,
            "lifecycle_mutated": False,
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
