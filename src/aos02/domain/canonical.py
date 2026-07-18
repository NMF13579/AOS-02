"""Deterministic serialization for binding canonical records."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(payload: Any) -> str:
    """Return stable UTF-8-safe JSON used only for deterministic bindings."""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def binding_digest(payload: Any) -> str:
    """Return SHA-256 digest of canonical JSON without granting authority."""
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
