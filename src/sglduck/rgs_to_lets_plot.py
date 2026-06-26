"""Assemble a lets-plot figure from a pgs and its per-layer DataFrames.

Ported from rsgl's ``rgs_to_ggplot2.R``. This slice covers single- and
multi-layer Cartesian plots with axis/legend titles, continuous scales, the
regression/jittered/unstacked qualifiers, and geom orientation. The remaining
pieces of ``rgs_to_ggplot2`` — facets and polar coordinates — land in follow-up
rendering PRs.
"""

from __future__ import annotations

import lets_plot

from .geom import SglGeomBox
from .lets_plot_direction import lets_plot_direction
from .titles import lets_plot_labs


def lets_plot_layer(layer: dict, df, scales: dict):
    """Build one lets-plot geom layer from a pgs layer and its DataFrame."""
    geom_expr = layer["geom_expr"]
    geom = geom_expr["geom"]
    qual = geom_expr["qual"]
    layer_args = {
        "data": df,
        "mapping": geom.lets_plot_aes(layer, df, scales),
    }
    # rsgl uses a smooth (linear-model) stat for the regression qualifier and an
    # identity stat for every other non-box geom; the box geom keeps its default
    # boxplot stat.
    if qual == "regression":
        layer_args["stat"] = "smooth"
        layer_args["method"] = "lm"
    elif not isinstance(geom, SglGeomBox):
        layer_args["stat"] = "identity"
    # The jittered/unstacked qualifiers select a non-default position.
    if qual == "jittered":
        layer_args["position"] = "jitter"
    elif qual == "unstacked":
        layer_args["position"] = "identity"
    # Direction-aware geoms (bar/line/box) carry an x/y orientation.
    if geom.has_direction():
        layer_args["orientation"] = lets_plot_direction(layer, df)
    return geom.lets_plot_geom()(**layer_args)


def rgs_to_lets_plot(pgs: dict, dfs: list):
    """Build the lets-plot figure for a pgs and its post-CTA per-layer frames."""
    scales = pgs.get("scales") or {}
    plot = lets_plot.ggplot()
    for layer, df in zip(pgs["layers"], dfs):
        plot += lets_plot_layer(layer, df, scales)
    for aes, scale in scales.items():
        for scale_feature in scale.lets_plot_scales(aes, pgs):
            plot += scale_feature
    plot += lets_plot_labs(pgs)
    return plot
