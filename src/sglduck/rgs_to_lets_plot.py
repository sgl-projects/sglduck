"""Assemble a lets-plot figure from a pgs and its per-layer DataFrames.

Ported from rsgl's ``rgs_to_ggplot2.R``. This covers single- and multi-layer
plots with axis/legend titles, continuous scales, the regression/jittered/
unstacked qualifiers, geom orientation, faceting, polar coordinates (the
``theta``/``r`` aesthetics), and single-positional-aesthetic plots whose unmapped
axis is blanked. The ``theta``/``r``-to-``x``/``y`` fold happens in
``SglGeom.lets_plot_aes``; this module adds the coordinate system and the
blank-axis handling on top.
"""

from __future__ import annotations

import lets_plot
import polars as pl

from .constants import BLANK_AES_COLUMN, POLAR_TO_CART_AES, POS_AES
from .geom import SglGeomBox
from .lets_plot_direction import lets_plot_direction
from .titles import lets_plot_labs


def _unmapped_cart_axes(layer: dict) -> set[str]:
    """The Cartesian axes (``"x"``/``"y"``) the layer leaves unmapped, after the
    theta/r fold."""
    mapped = {
        POLAR_TO_CART_AES.get(aes, aes)
        for aes in layer["aes_mappings"]
        if aes in POS_AES
    }
    return {"x", "y"} - mapped


def _blank_axis_features(layer: dict) -> list:
    """labs + theme features that hide a layer's unmapped positional axes.

    Mirrors rsgl's ``labs(<axis> = NULL)`` plus blank axis ticks: the axis only
    pins the data to a constant, so its title and ticks carry no meaning.
    """
    features = []
    for axis in sorted(_unmapped_cart_axes(layer)):
        features.append(lets_plot.labs(**{axis: ""}))
        features.append(
            lets_plot.theme(**{f"axis_ticks_{axis}": lets_plot.element_blank()})
        )
    return features


def lets_plot_layer(layer: dict, df, scales: dict):
    """Build one lets-plot geom layer from a pgs layer and its DataFrame."""
    geom_expr = layer["geom_expr"]
    geom = geom_expr["geom"]
    qual = geom_expr["qual"]
    # An unmapped positional aesthetic is pinned to a constant blank column;
    # lets-plot has no constant-aesthetic literal, so add it to the data.
    if _unmapped_cart_axes(layer):
        df = df.with_columns(pl.lit("").alias(BLANK_AES_COLUMN))
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


def lets_plot_facet(facets: list[dict]):
    """Build the lets-plot ``facet_grid`` feature from the pgs facets.

    Mirrors rsgl's ``ggplot_facet``: a single facet occupies columns
    (``x``, horizontal) or rows (``y``, vertical); two facets fill both axes,
    resolving which column is horizontal vs vertical from their directions. Two
    default facets put the second on columns and the first on rows; when only
    one direction is given the other facet takes the opposite axis.
    """
    if len(facets) == 1:
        column = facets[0]["column"]
        if facets[0]["direction"] in ("default", "horizontal"):
            return lets_plot.facet_grid(x=column)
        return lets_plot.facet_grid(y=column)

    directions = [facet["direction"] for facet in facets]
    columns = [facet["column"] for facet in facets]
    if set(directions) == {"default"}:
        horizontal_index, vertical_index = 1, 0
    elif set(directions) == {"horizontal", "vertical"}:
        horizontal_index = directions.index("horizontal")
        vertical_index = directions.index("vertical")
    elif "horizontal" in directions:
        horizontal_index = directions.index("horizontal")
        vertical_index = 1 - horizontal_index
    else:
        vertical_index = directions.index("vertical")
        horizontal_index = 1 - vertical_index
    return lets_plot.facet_grid(
        x=columns[horizontal_index],
        y=columns[vertical_index],
    )


def rgs_to_lets_plot(pgs: dict, dfs: list):
    """Build the lets-plot figure for a pgs and its post-CTA per-layer frames."""
    scales = pgs.get("scales") or {}
    plot = lets_plot.ggplot()
    for layer, df in zip(pgs["layers"], dfs):
        plot += lets_plot_layer(layer, df, scales)
    for feature in _blank_axis_features(pgs["layers"][0]):
        plot += feature
    for aes, scale in scales.items():
        for scale_feature in scale.lets_plot_scales(aes, pgs):
            plot += scale_feature
    # theta/r map onto x/y (the fold lives in lets_plot_aes); a theta mapping is
    # what makes the plot polar. All layers share the coordinate system, so the
    # first layer settles it.
    if "theta" in pgs["layers"][0]["aes_mappings"]:
        plot += lets_plot.coord_polar(theta="x")
    if "facets" in pgs:
        plot += lets_plot_facet(pgs["facets"])
    plot += lets_plot_labs(pgs)
    return plot
