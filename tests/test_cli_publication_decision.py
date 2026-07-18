import json
import subprocess
import sys

import yaml

from runtime_v2_fixtures import evidence, publication_decision, task


def test_cli_validates_human_publication_intent_without_granting_git_authority(tmp_path):
    for name, record in {
        "task": task(),
        "evidence": evidence(),
        "publication-decision": publication_decision(),
    }.items():
        (tmp_path / f"{name}.yaml").write_text(
            yaml.safe_dump(record, sort_keys=False), encoding="utf-8"
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
