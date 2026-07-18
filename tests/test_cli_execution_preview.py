import json
import subprocess
import sys

import yaml

from runtime_v2_fixtures import execution_decision, execution_request, task


def _write_execution_bundle(directory):
    for name, record in {
        "task": task(),
        "execution-decision": execution_decision(),
        "execution-request": execution_request(),
    }.items():
        (directory / f"{name}.yaml").write_text(
            yaml.safe_dump(record, sort_keys=False), encoding="utf-8"
        )


def test_cli_generates_non_mutating_execution_preview(tmp_path):
    _write_execution_bundle(tmp_path)

    result = subprocess.run([sys.executable, "-m", "aos02", "preview-execution", str(tmp_path)], capture_output=True, text=True, check=False)

    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["state"] == "PREVIEW_BLOCKED"
    assert payload["execution_readiness"] == "BLOCKED"
    assert payload["will_modify_files"] is False


def test_cli_executes_authorized_request_only_under_explicit_root(tmp_path):
    bundle = tmp_path / "bundle"
    root = tmp_path / "sandbox"
    bundle.mkdir()
    _write_execution_bundle(bundle)

    result = subprocess.run([sys.executable, "-m", "aos02", "execute-scoped", str(bundle), "--root", str(root)], capture_output=True, text=True, check=False)

    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["technical_status"] == "BLOCKED"
    assert "MUTATING_EXECUTOR_DISABLED" in payload["reason_codes"]
    assert not root.exists()
    assert not (root / "docs/example.md").exists()
    assert not (root / ".aos02").exists()
