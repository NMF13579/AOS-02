import json
import subprocess
import sys


def test_cli_validates_human_publication_intent_without_granting_git_authority(tmp_path):
    (tmp_path / "task.yaml").write_text("task_id: TASK-1\n")
    (tmp_path / "evidence.yaml").write_text("evidence_id: EVIDENCE-1\n")
    (tmp_path / "publication-decision.yaml").write_text(
        "record_type: HUMAN_PUBLICATION_DECISION\n"
        "decision_value: AUTHORIZE_PUBLICATION\n"
        "task_binding: TASK-1\n"
        "evidence_binding: EVIDENCE-1\n"
        "decided_by: HUMAN_OWNER\n"
    )

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "validate-publication", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["publication_decision_recorded"] is True
    assert payload["push_authorized"] is False
