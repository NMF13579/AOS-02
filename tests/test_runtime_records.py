from aos02.runtime_records import validate_runtime_record


def valid_evidence():
    return {
        "record_type": "EVIDENCE_REPORT",
        "schema_version": "1.0",
        "status": "PASS",
        "task_binding": "TASK-1",
        "reason_codes": [],
        "checks": [{"name": "scoped_execution", "status": "PASS"}],
        "operations": [{"path": "docs/example.md", "sha256": "a" * 64}],
        "evidence_artifact": {"path": ".aos02/evidence-report.json", "sha256": "b" * 64},
    }


def test_runtime_evidence_conforms_to_versioned_schema():
    result = validate_runtime_record(valid_evidence())

    assert result == {"valid": True, "reason_codes": []}


def test_runtime_evidence_rejects_unsafe_artifact_path():
    record = valid_evidence()
    record["evidence_artifact"]["path"] = "../evidence-report.json"

    result = validate_runtime_record(record)

    assert result["valid"] is False
    assert "SCHEMA_VALIDATION_FAILED" in result["reason_codes"]
