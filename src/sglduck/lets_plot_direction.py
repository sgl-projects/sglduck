"""Choose a layer's geom orientation (ported from rsgl's ``ggplot_orientation.R``).

Direction-aware geoms (bar/line/box) render along an ``"x"`` or ``"y"``
orientation. A direction qualifier (``horizontal``/``vertical``) picks it
directly; otherwise the orientation is inferred from the layer's positional
mappings — a single positional aesthetic fixes the perpendicular axis, a
collected box defers to its uncollected aesthetic, and the remaining cases rank
the two positional aesthetics by type (temporal, then categorical, then binned,
then numerical), with ties going to ``"x"``.
"""

from __future__ import annotations

import polars as pl

from .constants import CART_AES, POS_AES
from .geom import SglGeomBox
from .types import (
    is_binned_mapping,
    is_categorical_mapping,
    is_temporal_mapping,
)


def orntn_priority_ranking(layer: dict, df: pl.DataFrame, aes: str) -> int:
    """Rank an aesthetic's mapping for orientation (lower wins): temporal (1),
    categorical (2), binned (3), numerical/other (4)."""
    if is_temporal_mapping(layer, df, aes):
        return 1
    if is_categorical_mapping(layer, df, aes):
        return 2
    if is_binned_mapping(layer, aes):
        return 3
    return 4


def lets_plot_direction(layer: dict, df: pl.DataFrame) -> str:
    """The ``"x"``/``"y"`` orientation for a direction-aware layer's geom."""
    geom = layer["geom_expr"]["geom"]
    qual = layer["geom_expr"]["qual"]

    if qual in ("horizontal", "vertical"):
        return geom.lets_plot_dir_from_qual(qual)

    pos_mappings = {
        aes: col_expr
        for aes, col_expr in layer["aes_mappings"].items()
        if aes in POS_AES
    }

    # A single positional aesthetic orients along the perpendicular axis.
    if len(pos_mappings) == 1:
        pos_aes = next(iter(pos_mappings))
        return "y" if pos_aes in ("x", "theta") else "x"

    # A box with a collection on one positional aesthetic orients off the
    # uncollected one.
    if isinstance(geom, SglGeomBox) and "collections" in layer:
        collections = layer["collections"]
        uncollected_pos = {
            aes: col_expr
            for aes, col_expr in pos_mappings.items()
            if col_expr not in collections
        }
        if len(uncollected_pos) == 1:
            uncollected_aes = next(iter(uncollected_pos))
            return "y" if uncollected_aes in ("x", "theta") else "x"

    # Otherwise rank the two positional aesthetics by type; ties go to the first
    # axis ("x"/"theta").
    if next(iter(pos_mappings)) in CART_AES:
        first_rank = orntn_priority_ranking(layer, df, "x")
        second_rank = orntn_priority_ranking(layer, df, "y")
    else:
        first_rank = orntn_priority_ranking(layer, df, "theta")
        second_rank = orntn_priority_ranking(layer, df, "r")
    return "x" if first_rank <= second_rank else "y"
