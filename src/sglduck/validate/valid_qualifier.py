"""Validate a layer's geom qualifier."""

from __future__ import annotations

from ..constants import POS_AES
from ..errors import SglError
from ..geom import SglGeomBox


def expected_box_dir(ext_aes: str) -> str:
    """The box direction a positional aesthetic extends along."""
    if ext_aes in ("x", "theta"):
        return "horizontal"
    return "vertical"


def valid_box_direction(layer: dict) -> None:
    """Raise if the box direction qualifier conflicts with the mappings."""
    aes_mappings = layer["aes_mappings"]
    direction = layer["geom_expr"]["qual"]
    pos_mappings = {
        aes: mapping for aes, mapping in aes_mappings.items() if aes in POS_AES
    }
    if len(pos_mappings) == 1:
        (pos_aes,) = pos_mappings
        expected_dir = expected_box_dir(pos_aes)
        if direction != expected_dir:
            raise SglError(
                "Error: a single positional aesthetic"
                f" of {pos_aes} does not align with the {direction} qualifier"
                " for the box geom."
            )
    else:
        collections = layer.get("collections", [])
        uncollected_mappings = {
            aes: mapping
            for aes, mapping in pos_mappings.items()
            if mapping not in collections
        }
        if len(uncollected_mappings) == 1:
            (uncollected_aes,) = uncollected_mappings
            expected_dir = expected_box_dir(uncollected_aes)
            if direction != expected_dir:
                raise SglError(
                    "Error: a single uncollected positional aesthetic"
                    f" of {uncollected_aes} does not align with the {direction}"
                    " qualifier for the box geom."
                )


def valid_qualifier(layer: dict) -> None:
    """Raise if the layer's qualifier is invalid for its geom."""
    geom = layer["geom_expr"]["geom"]
    qual = layer["geom_expr"]["qual"]
    if qual == "default":
        return
    if qual not in geom.valid_qual_list():
        raise SglError(
            f"Error: the {qual} qualifier is not valid for the"
            f" {geom.geom_name()} geom."
        )
    if geom == SglGeomBox():
        valid_box_direction(layer)
