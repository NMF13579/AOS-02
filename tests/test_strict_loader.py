from pathlib import Path

import pytest

from aos02.__main__ import load_records
from runtime_v2_fixtures import execution_request, task


def _write(path: Path, text: str = "task_id: TASK-1\n") -> None:
    path.write_text(text, encoding="utf-8")


def test_loader_accepts_only_required_records_from_a_known_closed_world(tmp_path):
    import yaml

    _write(tmp_path / "task.yaml", yaml.safe_dump(task(), sort_keys=False))
    _write(
        tmp_path / "execution-request.yaml",
        yaml.safe_dump(execution_request(), sort_keys=False),
    )

    records = load_records(tmp_path, ("task",))

    assert records["task"] == task()
    assert records["execution-request"] == execution_request()


@pytest.mark.parametrize("name", ["notes.txt", "task.yml", "Idea.yaml"])
def test_loader_rejects_unknown_or_noncanonical_bundle_entries(tmp_path, name):
    _write(tmp_path / "task.yaml")
    _write(tmp_path / name)

    with pytest.raises(ValueError, match="unknown bundle entry"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_bundle_subdirectories(tmp_path):
    _write(tmp_path / "task.yaml")
    (tmp_path / "nested").mkdir()

    with pytest.raises(ValueError, match="regular non-symlink file"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_symlinked_records(tmp_path):
    target = tmp_path / "risk.yaml"
    _write(target)
    (tmp_path / "task.yaml").symlink_to(target)

    with pytest.raises(ValueError, match="regular non-symlink file"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_duplicate_yaml_keys(tmp_path):
    _write(tmp_path / "task.yaml", "task_id: TASK-1\ntask_id: TASK-2\n")

    with pytest.raises(ValueError, match="duplicate YAML key"):
        load_records(tmp_path, ("task",))


@pytest.mark.parametrize(
    "yaml_text",
    [
        "task_id: &task TASK-1\ncopy: *task\n",
        "defaults: &defaults\n  task_id: TASK-1\ncopy:\n  <<: *defaults\n",
    ],
)
def test_loader_rejects_yaml_anchors_aliases_and_merges(tmp_path, yaml_text):
    _write(tmp_path / "task.yaml", yaml_text)

    with pytest.raises(ValueError, match="anchors and aliases are forbidden"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_custom_yaml_tags(tmp_path):
    _write(tmp_path / "task.yaml", "task_id: !unsafe TASK-1\n")

    with pytest.raises(ValueError, match="invalid YAML"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_multiple_yaml_documents(tmp_path):
    _write(tmp_path / "task.yaml", "task_id: TASK-1\n---\ntask_id: TASK-2\n")

    with pytest.raises(ValueError, match="invalid YAML"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_non_string_mapping_keys(tmp_path):
    _write(tmp_path / "task.yaml", "1: task\n")

    with pytest.raises(ValueError, match="YAML mapping keys must be strings"):
        load_records(tmp_path, ("task",))


def test_loader_validates_recognized_extra_records_before_dispatch(tmp_path):
    _write(tmp_path / "task.yaml")
    _write(tmp_path / "execution-request.yaml", "record_type: [\n")

    with pytest.raises(ValueError, match="invalid YAML"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_oversized_yaml_before_parsing(tmp_path, monkeypatch):
    from aos02 import loader

    monkeypatch.setattr(loader, "MAX_DOCUMENT_BYTES", 32)
    _write(tmp_path / "task.yaml", "x: " + "a" * 40)

    with pytest.raises(ValueError, match="document exceeds maximum size"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_excessive_mapping_nesting(tmp_path, monkeypatch):
    from aos02 import loader

    monkeypatch.setattr(loader, "MAX_NESTING_DEPTH", 2)
    _write(tmp_path / "task.yaml", "a:\n  b:\n    c: value\n")

    with pytest.raises(ValueError, match="nesting depth exceeds maximum"):
        load_records(tmp_path, ("task",))


def test_loader_rejects_oversized_collection(tmp_path, monkeypatch):
    from aos02 import loader

    monkeypatch.setattr(loader, "MAX_COLLECTION_ITEMS", 2)
    _write(tmp_path / "task.yaml", "items: [one, two, three]\n")

    with pytest.raises(ValueError, match="collection exceeds maximum size"):
        load_records(tmp_path, ("task",))
