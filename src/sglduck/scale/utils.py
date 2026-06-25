"""Helpers shared across the scale classes."""

from __future__ import annotations

import lets_plot
import polars as pl

from ..errors import SglError
from ..geom import SglGeomBar
from ..types import is_categorical_mapping, is_temporal_mapping
from ..utils import col_expr_has_cta, column_from_aes


def non_numerical_in_layer(aes: str, layer: dict, df: pl.DataFrame) -> bool:
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


def non_pos_in_layer(aes: str, layer: dict, df: pl.DataFrame) -> bool:
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


# Positional aesthetics fold onto the Cartesian axes; theta -> x, r -> y.
_POSITION_SCALE = {
    "x": lets_plot.scale_x_continuous,
    "theta": lets_plot.scale_x_continuous,
    "y": lets_plot.scale_y_continuous,
    "r": lets_plot.scale_y_continuous,
}
_COLOR_SCALE = {
    "color": lets_plot.scale_color_continuous,
    "fill": lets_plot.scale_fill_continuous,
}


def lets_plot_color_aes(pgs: dict) -> list[str]:
    """The lets-plot color aesthetics for the color-mapped layers.

    A bar layer maps color onto ``fill``; every other geom maps it onto
    ``color``. The result is de-duplicated in first-seen order.
    """
    color_aes = [
        "fill" if isinstance(layer["geom_expr"]["geom"], SglGeomBar) else "color"
        for layer in pgs["layers"]
        if "color" in layer["aes_mappings"]
    ]
    return list(dict.fromkeys(color_aes))


def lets_plot_continuous_scales(transform: str, aes: str, pgs: dict) -> list:
    """The lets-plot continuous scale(s) applying ``transform`` to an aesthetic.

    A positional or size aesthetic yields a single scale; the color aesthetic
    yields a fill and/or color scale, one per distinct color aesthetic across the
    color-mapped layers.
    """
    if aes in _POSITION_SCALE:
        scale_fns = [_POSITION_SCALE[aes]]
    elif aes == "size":
        scale_fns = [lets_plot.scale_size]
    elif aes == "color":
        scale_fns = [_COLOR_SCALE[color_aes] for color_aes in lets_plot_color_aes(pgs)]
    return [scale_fn(trans=transform) for scale_fn in scale_fns]
