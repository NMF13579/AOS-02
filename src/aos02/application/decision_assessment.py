"""Transitional application façade for result and publication assessment."""

from ..publication_decision import validate_human_publication_decision
from ..result_decision import validate_human_result_decision

__all__ = ["validate_human_publication_decision", "validate_human_result_decision"]
