"""Validate a layer's aesthetic mappings."""

from __future__ import annotations

from ..constants import CART_AES, POLAR_AES, POS_AES
from ..errors import SglError


def valid_aesthetics(layer: dict) -> None:
    """Raise if the layer's aesthetics are positionally or geom-invalid."""
    geom = layer["geom_expr"]["geom"]
    actual_aes_names = list(layer["aes_mappings"])
    cart_coords_found = [aes for aes in actual_aes_names if aes in CART_AES]
    polar_coords_found = [aes for aes in actual_aes_names if aes in POLAR_AES]

    if not cart_coords_found and not polar_coords_found:
        raise SglError(
            "Error: positional mapping(s) must be provided, none were found."
        )

    if cart_coords_found and polar_coords_found:
        raise SglError(
            "Error: found aesthetics from multiple coordinate systems."
            " All positional aesthetics must be from a single coordinate system."
        )

    non_pos_aes_found = [aes for aes in actual_aes_names if aes not in POS_AES]
    invalid_non_pos_aes = [
        aes for aes in non_pos_aes_found if aes not in geom.valid_non_pos_aes()
    ]
    if invalid_non_pos_aes:
        raise SglError(
            f"Error: the {invalid_non_pos_aes[0]} aesthetic is not valid"
            f" for the {geom.geom_name()} geom."
        )
