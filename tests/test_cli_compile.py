import json
import subprocess
import sys


def test_cli_compiles_task_brief_draft_from_bundle(tmp_path):
    source = """idea_id: IDEA-1
unknowns: []
"""
    (tmp_path / "idea.yaml").write_text(source)
    (tmp_path / "risk.yaml").write_text("risk_id: RISK-1\nidea_binding: IDEA-1\n")
    (tmp_path / "scope.yaml").write_text("scope_id: SCOPE-1\nidea_binding: IDEA-1\nallowed_paths: [docs/example.md]\nforbidden_paths: [src/]\n")

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "compile-task", str(tmp_path), "--task-id", "TASK-1", "--check", "markdown"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "DRAFT"
    assert payload["human_decision_required"] is True
    assert payload["execution_authorized"] is False
