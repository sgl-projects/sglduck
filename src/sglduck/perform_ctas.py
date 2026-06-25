"""Run each layer's column transformations and aggregations.

Ported from rsgl's ``perform_ctas.R``. This is the render-time data step: for
each pgs layer, apply its transformation CTAs (binning) and then its
aggregation CTAs (avg/count), producing the DataFrame the renderer plots.
"""

from __future__ import annotations

import polars as pl

from .perform_as_for_layer import perform_as_for_layer
from .perform_cts_for_layer import perform_cts_for_layer


def perform_ctas_for_layer(
    layer: dict, df: pl.DataFrame, scales: dict | None
) -> pl.DataFrame:
    """Apply one layer's transformations then aggregations."""
    post_ct_df = perform_cts_for_layer(layer, df, scales)
    return perform_as_for_layer(layer, post_ct_df, scales)


def perform_ctas(pgs: dict, dfs: list[pl.DataFrame]) -> list[pl.DataFrame]:
    """Apply each layer's CTAs to its DataFrame, returning one frame per layer."""
    scales = pgs.get("scales")
    return [
        perform_ctas_for_layer(layer, df, scales)
        for layer, df in zip(pgs["layers"], dfs)
    ]
