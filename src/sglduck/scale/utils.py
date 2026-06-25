"""Helpers shared across the scale classes."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from ..types import is_categorical_mapping, is_temporal_mapping
from ..utils import col_expr_has_cta, column_from_aes


def non_numerical_in_layer(aes: str, layer: dict, df: pd.DataFrame) -> bool:
    """Whether the layer maps the aesthetic to a non-numerical column."""
    if aes in layer["aes_mappings"]:
        if is_categorical_mapping(layer, df, aes) or is_temporal_mapping(
            layer, df, aes
        ):
            return True
    return False


def raise_for_non_nums(scale, aes: str, layers: list[dict], dfs) -> None:
    """Raise if any layer maps the scaled aesthetic non-numerically."""
    if any(
        non_numerical_in_layer(aes, layer, df) for layer, df in zip(layers, dfs)
    ):
        raise SglError(
            f"Error: the {scale.sgl_func_name()} scale can only be applied"
            " to aesthetics with numerical mappings."
        )


def non_pos_in_layer(aes: str, layer: dict, df: pd.DataFrame) -> bool:
    """Whether the layer maps the aesthetic to non-positive values."""
    aes_mappings = layer["aes_mappings"]
    if aes in aes_mappings:
        col_expr = aes_mappings[aes]
        if not col_expr_has_cta(col_expr, "count"):
            col = column_from_aes(layer, df, aes)
            if (col <= 0).any():
                return True
    return False


def raise_for_non_pos(scale, aes: str, layers: list[dict], dfs) -> None:
    """Raise if any layer maps the scaled aesthetic to non-positive values."""
    if any(non_pos_in_layer(aes, layer, df) for layer, df in zip(layers, dfs)):
        raise SglError(
            f"Error: the {scale.sgl_func_name()} scale can only be applied to"
            " aesthetics where all values from mappings are positive."
        )
