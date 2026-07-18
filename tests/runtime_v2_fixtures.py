BASELINE = "git:69b0d85ccf4d8cee53d6497941b84614d2951375"


def idea():
    return {
        "record_type": "IDEA_RECORD",
        "schema_version": "2.0",
        "idea_id": "IDEA-1",
        "unknowns": [],
    }


def risk():
    return {
        "record_type": "RISK_PROFILE",
        "schema_version": "2.0",
        "risk_id": "RISK-1",
        "idea_binding": "IDEA-1",
        "baseline_binding": BASELINE,
        "selected_level": "HIGH_RISK_PROTECTED",
        "decided_by": "HUMAN_OWNER",
        "identity_assurance_level": "LOCAL_DECLARED_HUMAN_REFERENCE",
    }


def scope():
    return {
        "record_type": "SCOPE_AND_CHANGE",
        "schema_version": "2.0",
        "scope_id": "SCOPE-1",
        "idea_binding": "IDEA-1",
        "baseline_binding": BASELINE,
        "allowed_paths": ["docs/example.md"],
        "forbidden_paths": ["src/blocked.py"],
    }


def task():
    return {
        "record_type": "TASK_BRIEF",
        "schema_version": "2.0",
        "status": "DRAFT",
        "task_id": "TASK-1",
        "idea_binding": "IDEA-1",
        "risk_binding": "RISK-1",
        "scope_binding": "SCOPE-1",
        "baseline_binding": BASELINE,
        "allowed_paths": ["docs/example.md"],
        "forbidden_paths": ["src/blocked.py"],
        "required_checks": ["markdown"],
    }


def evidence():
    return {
        "record_type": "EVIDENCE_REPORT",
        "schema_version": "2.0",
        "evidence_id": "EVIDENCE-1",
        "task_binding": "TASK-1",
        "baseline_binding": BASELINE,
        "technical_status": "PASS",
        "reason_codes": [],
        "checks": [
            {
                "name": "markdown",
                "status": "PASS",
                "exit_code": 0,
                "output_reference": "inline:test",
            }
        ],
        "unknowns": [],
        "not_run": [],
        "blockers": [],
    }


def execution_decision():
    return {
        "record_type": "HUMAN_DECISION_RECORD",
        "schema_version": "2.0",
        "status": "HUMAN_ACCEPTED",
        "decision_id": "DECISION-EXECUTION-1",
        "decision_type": "EXECUTION",
        "decided_by": "HUMAN_OWNER",
        "identity_assurance_level": "LOCAL_DECLARED_HUMAN_REFERENCE",
        "scope_binding": "TASK-1",
        "baseline_binding": BASELINE,
        "decision_value": "ALLOW_LOCAL_EXECUTION",
        "grants": ["LOCAL_EXECUTION"],
        "non_grants": ["COMMIT", "PUSH", "MERGE", "RELEASE"],
    }


def execution_request():
    return {
        "record_type": "EXECUTION_REQUEST",
        "schema_version": "2.0",
        "task_binding": "TASK-1",
        "baseline_binding": BASELINE,
        "operations": [
            {"action": "WRITE", "path": "docs/example.md", "content": "safe content\n"}
        ],
    }


def result_decision():
    return {
        "record_type": "HUMAN_DECISION_RECORD",
        "schema_version": "2.0",
        "status": "HUMAN_ACCEPTED",
        "decision_id": "DECISION-RESULT-1",
        "decision_type": "RESULT_ACCEPTANCE",
        "decided_by": "HUMAN_OWNER",
        "identity_assurance_level": "LOCAL_DECLARED_HUMAN_REFERENCE",
        "scope_binding": "TASK-1",
        "evidence_binding": "EVIDENCE-1",
        "baseline_binding": BASELINE,
        "decision_value": "ACCEPT",
        "grants": ["RESULT_ACCEPTANCE"],
        "non_grants": ["COMMIT", "PUSH", "MERGE", "RELEASE"],
    }


def publication_decision():
    return {
        "record_type": "HUMAN_DECISION_RECORD",
        "schema_version": "2.0",
        "status": "HUMAN_ACCEPTED",
        "decision_id": "DECISION-PUSH-1",
        "decision_type": "PUSH",
        "decided_by": "HUMAN_OWNER",
        "identity_assurance_level": "LOCAL_DECLARED_HUMAN_REFERENCE",
        "scope_binding": "TASK-1",
        "evidence_binding": "EVIDENCE-1",
        "baseline_binding": BASELINE,
        "decision_value": "AUTHORIZE_PUBLICATION",
        "grants": ["PUSH"],
        "non_grants": ["COMMIT", "MERGE", "RELEASE"],
    }


def execution_preview():
    return {
        "record_type": "EXECUTION_PREVIEW",
        "schema_version": "2.0",
        "task_binding": "TASK-1",
        "baseline_binding": BASELINE,
        "state": "PREVIEW_BLOCKED",
        "execution_readiness": "BLOCKED",
        "reason_codes": ["TRUSTED_HUMAN_AUTHORITY_NOT_IMPLEMENTED"],
        "will_modify_files": False,
        "operation_count": 1,
        "operations": [{"action": "WRITE", "path": "docs/example.md"}],
    }


def execution_outcome():
    return {
        "record_type": "EXECUTION_OUTCOME",
        "schema_version": "2.0",
        "task_binding": "TASK-1",
        "baseline_binding": BASELINE,
        "technical_status": "BLOCKED",
        "reason_codes": ["MUTATING_EXECUTOR_DISABLED"],
        "checks": [{"name": "scoped_execution", "status": "NOT_RUN"}],
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
    }


def full_bundle():
    return {
        "idea": idea(),
        "risk": risk(),
        "scope": scope(),
        "task": task(),
        "evidence": evidence(),
        "execution-decision": execution_decision(),
        "execution-request": execution_request(),
        "result-decision": result_decision(),
        "publication-decision": publication_decision(),
    }
