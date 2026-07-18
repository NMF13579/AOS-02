import json
import subprocess
import sys

import yaml

from test_validation import valid_bundle


def test_cli_validates_yaml_bundle_without_authority_claim(tmp_path):
    for name, record in valid_bundle().items():
        (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump(record, sort_keys=False))

    result = subprocess.run(
        [sys.executable, "-m", "aos02", "validate", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["validation"]["status"] == "PASS"
    assert payload["control"]["state"] == "CONTROL_HUMAN_REVIEW_REQUIRED"
    assert payload["approval_granted"] is False
