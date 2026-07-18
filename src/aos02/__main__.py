"""Read-only CLI adapter for AOS-02 canonical record bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from .task_brief import TaskBriefError, compile_task_brief
from .validation import validate_bundle

REQUIRED_RECORDS = ("idea", "risk", "scope", "task", "evidence")
TASK_SOURCE_RECORDS = ("idea", "risk", "scope")


def load_records(directory: Path, required_records: tuple[str, ...]) -> dict[str, Any]:
    if not directory.is_dir():
        raise ValueError(f"bundle directory does not exist: {directory}")
    bundle: dict[str, Any] = {}
    for name in required_records:
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
    compile_task = subcommands.add_parser("compile-task", help="compile a non-authoritative Task Brief draft")
    compile_task.add_argument("bundle", type=Path)
    compile_task.add_argument("--task-id", required=True)
    compile_task.add_argument("--check", action="append", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_bundle(load_records(args.bundle, REQUIRED_RECORDS))
        else:
            records = load_records(args.bundle, TASK_SOURCE_RECORDS)
            result = compile_task_brief(
                idea=records["idea"], risk=records["risk"], scope=records["scope"],
                task_id=args.task_id, required_checks=args.check,
            )
    except (OSError, ValueError, TaskBriefError, yaml.YAMLError) as exc:
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
