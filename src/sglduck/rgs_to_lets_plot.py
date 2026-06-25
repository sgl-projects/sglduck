"""Assemble a lets-plot figure from a pgs and its per-layer DataFrames.

Ported from rsgl's ``rgs_to_ggplot2.R``. This slice covers single- and
multi-layer Cartesian plots with the default qualifier, plus axis/legend titles.
The remaining pieces of ``rgs_to_ggplot2`` — scales, facets, polar coordinates,
the regression/jitter/unstacked qualifiers and geom orientation — land in
follow-up rendering PRs.
"""

from __future__ import annotations

import lets_plot

from .geom import SglGeomBox
from .titles import lets_plot_labs


def lets_plot_layer(layer: dict, df, scales: dict):
    """Build one lets-plot geom layer from a pgs layer and its DataFrame."""
    geom = layer["geom_expr"]["geom"]
    layer_args = {
        "data": df,
        "mapping": geom.lets_plot_aes(layer, df, scales),
    }
    # rsgl forces an identity stat for every non-box geom; the box geom keeps its
    # default boxplot stat. (Qualifier-driven stats/positions arrive later.)
    if not isinstance(geom, SglGeomBox):
        layer_args["stat"] = "identity"
    return geom.lets_plot_geom()(**layer_args)


def rgs_to_lets_plot(pgs: dict, dfs: list):
    """Build the lets-plot figure for a pgs and its post-CTA per-layer frames."""
    scales = pgs.get("scales") or {}
    plot = lets_plot.ggplot()
    for layer, df in zip(pgs["layers"], dfs):
        plot += lets_plot_layer(layer, df, scales)
    plot += lets_plot_labs(pgs)
    return plot
