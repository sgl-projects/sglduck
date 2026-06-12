"""Validate the pgs titles against the layer mappings."""

from __future__ import annotations

from ..errors import SglError
from ..utils import all_aesthetics


def valid_titles(pgs: dict) -> None:
    """Raise if any title targets an aesthetic no layer maps."""
    all_aes_in_mappings = all_aesthetics(pgs)
    for titled_aes in pgs.get("titles", {}):
        if titled_aes not in all_aes_in_mappings:
            raise SglError(
                "Error: title provided for aesthetic not found"
                f" in any layer's aesthetic mapping: {titled_aes}."
            )
