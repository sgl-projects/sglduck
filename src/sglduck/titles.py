"""Resolve axis/legend titles and build the lets-plot ``labs`` (ported from titles.R).

A title for an aesthetic is the one given in the ``title`` clause, or — failing
that — the textual form of the first layer's column expression for that aesthetic
(``hp``, ``avg(hp)``, ``bin(mpg, 10)``, ...). ``theta``/``r`` fold onto the ``x``/
``y`` labels; the ``color`` aesthetic splits into a ``fill`` legend title for bar
layers and a ``color`` legend title for every other geom (bars remap color onto
fill).
"""

from __future__ import annotations

import lets_plot

from .geom import SglGeomBar
from .utils import all_aesthetics

# theta/r fold onto the Cartesian x/y axis labels.
_POLAR_TO_CART = {"theta": "x", "r": "y"}


def default_title(col_expr: dict) -> str:
    """The textual form of a column expression, e.g. ``avg(hp)`` or ``bin(mpg, 10)``."""
    return col_expr["cta"].expr_text(col_expr)


def title_for_aes(aes: str, pgs: dict) -> str | None:
    """The explicit title for an aesthetic, else its first layer's default title."""
    titles = pgs.get("titles") or {}
    if aes in titles:
        return titles[aes]
    for layer in pgs["layers"]:
        if aes in layer["aes_mappings"]:
            return default_title(layer["aes_mappings"][aes])
    return None


def _color_labs_args(pgs: dict) -> dict:
    """Split color-mapped layers into a ``fill`` (bar) and ``color`` (non-bar) title.

    Bars remap the color aesthetic onto fill, so a bar layer's color title becomes
    the fill legend title while every other geom's becomes the color legend title.
    """
    bar_layers = []
    non_bar_layers = []
    for layer in pgs["layers"]:
        if "color" in layer["aes_mappings"]:
            if isinstance(layer["geom_expr"]["geom"], SglGeomBar):
                bar_layers.append(layer)
            else:
                non_bar_layers.append(layer)

    args = {}
    if bar_layers:
        args["fill"] = title_for_aes("color", {**pgs, "layers": bar_layers})
    if non_bar_layers:
        args["color"] = title_for_aes("color", {**pgs, "layers": non_bar_layers})
    return args


def labs_args(pgs: dict) -> dict:
    """The aesthetic -> title mapping for the plot's labels."""
    all_aes = all_aesthetics(pgs)
    args = {
        _POLAR_TO_CART.get(aes, aes): title_for_aes(aes, pgs)
        for aes in all_aes
        if aes != "color"
    }
    if "color" in all_aes:
        args.update(_color_labs_args(pgs))
    return args


def lets_plot_labs(pgs: dict):
    """Build the lets-plot ``labs`` feature for the plot."""
    return lets_plot.labs(**labs_args(pgs))
