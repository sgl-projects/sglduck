"""Validate a layer's collect by clause."""

from __future__ import annotations

from ..constants import NON_POS_AES, POS_AES
from ..errors import SglError


def valid_collections(layer: dict) -> None:
    """Raise if the layer's collections are invalid for its geom."""
    if "collections" not in layer:
        return

    aes_mappings = layer["aes_mappings"]
    geom = layer["geom_expr"]["geom"]
    collections = layer["collections"]

    if not geom.is_collective():
        raise SglError(
            "Error: collect by clause should not be provided"
            f" for non-collective geom {geom.geom_name()}."
        )

    non_pos_mappings = [
        mapping for aes, mapping in aes_mappings.items() if aes in NON_POS_AES
    ]
    if not all(mapping in collections for mapping in non_pos_mappings):
        raise SglError(
            "Error: all expressions mapped to from non-positional"
            " aesthetics must be included in the collect by clause."
        )

    pos_mappings = [
        mapping for aes, mapping in aes_mappings.items() if aes in POS_AES
    ]
    uncollected_pos = [
        mapping for mapping in pos_mappings if mapping not in collections
    ]
    if len(uncollected_pos) > geom.extension():
        raise SglError(
            "Error: the number of uncollected positional aesthetic"
            f" expressions exceeds the extensionality of the {geom.geom_name()}"
            " geom. Add an expression mapped to from a positional aesthetic"
            " to the collect by clause."
        )
