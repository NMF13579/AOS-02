import json
import subprocess
import sys

import yaml

from runtime_v2_fixtures import idea, risk, scope


def test_cli_compiles_task_brief_draft_from_bundle(tmp_path):
    for name, record in {"idea": idea(), "risk": risk(), "scope": scope()}.items():
        (tmp_path / f"{name}.yaml").write_text(
            yaml.safe_dump(record, sort_keys=False), encoding="utf-8"
        )

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "compile-task", str(tmp_path), "--task-id", "TASK-1", "--check", "markdown"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "DRAFT"
    assert payload["schema_version"] == "2.0"
    assert payload["human_decision_required"] is True
    assert payload["execution_authorized"] is False
