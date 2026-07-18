from pathlib import Path

from aos02.execution import execute_scoped_request


def task():
    return {"task_id": "TASK-1", "allowed_paths": ["docs/example.md"]}


def decision(value="ALLOW_LOCAL_EXECUTION"):
    return {
        "record_type": "HUMAN_EXECUTION_DECISION",
        "decision_value": value,
        "task_binding": "TASK-1",
        "decided_by": "HUMAN_OWNER",
        "allowed_paths": ["docs/example.md"],
    }


def request(path="docs/example.md"):
    return {
        "record_type": "EXECUTION_REQUEST",
        "task_binding": "TASK-1",
        "operations": [{"action": "WRITE", "path": path, "content": "safe content\n"}],
    }


def test_direct_execution_is_disabled_without_creating_target_or_evidence(tmp_path):
    root = tmp_path / "sandbox"

    result = execute_scoped_request(root=root, task=task(), decision=decision(), request=request())

    assert result["status"] == "BLOCKED"
    assert "MUTATING_EXECUTOR_DISABLED" in result["reason_codes"]
    assert not root.exists()
    assert not (root / "docs/example.md").exists()
    assert not (root / ".aos02").exists()


def test_direct_execution_does_not_mutate_an_existing_sandbox(tmp_path):
    root = tmp_path / "sandbox"
    root.mkdir()
    sentinel = root / "sentinel.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8")
    before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))

    result = execute_scoped_request(root=root, task=task(), decision=decision("DENY"), request=request())

    after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
    assert result["status"] == "BLOCKED"
    assert sentinel.read_text(encoding="utf-8") == "unchanged\n"
    assert after == before
    assert not (root / ".aos02").exists()


def test_direct_execution_never_uses_root_object():
    class RootThatRaisesOnAccess:
        def __getattribute__(self, name):
            raise AssertionError(f"root access is forbidden: {name}")

    result = execute_scoped_request(
        root=RootThatRaisesOnAccess(), task=task(), decision=decision(), request=request()
    )

    assert result["status"] == "BLOCKED"
    assert result["checks"] == [{"name": "scoped_execution", "status": "NOT_RUN"}]
