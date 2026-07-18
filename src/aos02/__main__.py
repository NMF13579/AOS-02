"""Read-only CLI adapter for AOS-02 canonical record bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .execution import execute_scoped_request
from .execution_decision import validate_human_execution_decision
from .execution_preview import preview_scoped_execution
from .loader import load_records
from .publication_decision import validate_human_publication_decision
from .result_decision import validate_human_result_decision
from .task_brief import TaskBriefError, compile_task_brief
from .validation import validate_bundle

REQUIRED_RECORDS = ("idea", "risk", "scope", "task", "evidence")
TASK_SOURCE_RECORDS = ("idea", "risk", "scope")
RESULT_DECISION_RECORDS = ("task", "evidence", "result-decision")
PUBLICATION_DECISION_RECORDS = ("task", "evidence", "publication-decision")
EXECUTION_DECISION_RECORDS = ("task", "execution-decision")
EXECUTION_PREVIEW_RECORDS = ("task", "execution-decision", "execution-request")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aos02", description="AOS-02 read-only control validation")
    subcommands = parser.add_subparsers(dest="command", required=True)
    validate = subcommands.add_parser("validate", help="validate a canonical YAML record bundle")
    validate.add_argument("bundle", type=Path)
    compile_task = subcommands.add_parser("compile-task", help="compile a non-authoritative Task Brief draft")
    compile_task.add_argument("bundle", type=Path)
    compile_task.add_argument("--task-id", required=True)
    compile_task.add_argument("--check", action="append", required=True)
    validate_result = subcommands.add_parser("validate-result", help="validate a Human Result Decision")
    validate_result.add_argument("bundle", type=Path)
    validate_publication = subcommands.add_parser("validate-publication", help="validate a Human Publication Decision without Git authority")
    validate_publication.add_argument("bundle", type=Path)
    validate_execution = subcommands.add_parser("validate-execution", help="validate a Human Execution Decision")
    validate_execution.add_argument("bundle", type=Path)
    preview_execution = subcommands.add_parser("preview-execution", help="produce a non-mutating scoped execution preview")
    preview_execution.add_argument("bundle", type=Path)
    execute_scoped = subcommands.add_parser("execute-scoped", help="execute an authorized request only below an explicit sandbox root")
    execute_scoped.add_argument("bundle", type=Path)
    execute_scoped.add_argument("--root", type=Path, required=True, help="explicit sandbox root for all file writes")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_bundle(load_records(args.bundle, REQUIRED_RECORDS))
        elif args.command == "compile-task":
            records = load_records(args.bundle, TASK_SOURCE_RECORDS)
            result = compile_task_brief(
                idea=records["idea"], risk=records["risk"], scope=records["scope"],
                task_id=args.task_id, required_checks=args.check,
            )
        elif args.command == "validate-result":
            records = load_records(args.bundle, RESULT_DECISION_RECORDS)
            result = validate_human_result_decision(
                task=records["task"], evidence=records["evidence"], decision=records["result-decision"],
            )
        elif args.command == "validate-publication":
            records = load_records(args.bundle, PUBLICATION_DECISION_RECORDS)
            result = validate_human_publication_decision(
                task=records["task"], evidence=records["evidence"], decision=records["publication-decision"],
            )
        elif args.command == "validate-execution":
            records = load_records(args.bundle, EXECUTION_DECISION_RECORDS)
            result = validate_human_execution_decision(
                task=records["task"], decision=records["execution-decision"],
            )
        elif args.command == "preview-execution":
            records = load_records(args.bundle, EXECUTION_PREVIEW_RECORDS)
            result = preview_scoped_execution(
                task=records["task"], decision=records["execution-decision"], request=records["execution-request"],
            )
        else:
            records = load_records(args.bundle, EXECUTION_PREVIEW_RECORDS)
            result = execute_scoped_request(
                root=args.root, task=records["task"], decision=records["execution-decision"], request=records["execution-request"],
            )
    except (OSError, ValueError, TaskBriefError) as exc:
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
    if result.get("validation", {}).get("status") == "FAIL":
        return 3
    if args.command in {"validate-execution", "preview-execution", "execute-scoped"}:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
