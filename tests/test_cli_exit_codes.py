"""CLI semantic and unexpected-error exits are fail closed."""

import json

import aos02.interfaces.cli as cli


def test_validate_not_run_returns_semantic_failure_exit(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "load_records", lambda *_: {"ignored": {}})
    monkeypatch.setattr(
        cli,
        "validate_bundle",
        lambda _: {"validation": {"status": "NOT_RUN"}, "control": {"state": "CONTROL_BLOCKED"}},
    )

    assert cli.main(["validate", "unused"]) == 3
    assert json.loads(capsys.readouterr().out)["validation"]["status"] == "NOT_RUN"


def test_validate_execution_structural_failure_returns_semantic_failure_exit(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "load_records", lambda *_: {"task": {}, "execution-decision": {}})
    monkeypatch.setattr(
        cli,
        "validate_human_execution_decision",
        lambda **_: {"structural_validation": {"status": "FAIL"}, "authority_validation": {"status": "UNTRUSTED"}},
    )

    assert cli.main(["validate-execution", "unused"]) == 3
    assert json.loads(capsys.readouterr().out)["structural_validation"]["status"] == "FAIL"


def test_unexpected_error_returns_json_exit_five_without_free_text_reason_code(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "load_records", lambda *_: (_ for _ in ()).throw(RuntimeError("secret detail")))

    assert cli.main(["validate", "unused"]) == 5
    result = json.loads(capsys.readouterr().out)
    assert result["reason_codes"] == ["INTERNAL_ERROR"]
    assert result["diagnostic_detail"] == "RuntimeError"
