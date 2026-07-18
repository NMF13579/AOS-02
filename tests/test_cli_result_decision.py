import json
import subprocess
import sys


def test_cli_validates_bound_human_result_decision(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\n")
    (tmp_path / "evidence.yaml").write_text(
        "evidence_id: EVIDENCE-1\ntask_binding: TASK-1\nchecks:\n  - name: markdown\n    status: PASS\nunknowns: []\nnot_run: []\n"
    )
    (tmp_path / "result-decision.yaml").write_text(
        "record_type: HUMAN_RESULT_DECISION\ndecision_value: ACCEPT\ntask_binding: TASK-1\nevidence_binding: EVIDENCE-1\ndecided_by: HUMAN_OWNER\n"
    )

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "validate-result", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["result_accepted"] is True
    assert payload["push_authorized"] is False
