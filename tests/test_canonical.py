import hashlib

from aos02.canonical import binding_digest, canonical_json


def test_binding_digest_is_stable_across_mapping_order():
    first = {"record_type": "IDEA", "unknowns": ["repository state"]}
    second = {"unknowns": ["repository state"], "record_type": "IDEA"}

    assert canonical_json(first) == '{"record_type":"IDEA","unknowns":["repository state"]}'
    assert binding_digest(first) == binding_digest(second)
    assert binding_digest(first) == hashlib.sha256(canonical_json(first).encode()).hexdigest()
