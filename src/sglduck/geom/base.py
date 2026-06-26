"""Base class for SGL geoms.

As with CTAs, a geom's behaviour lives in methods on the class hierarchy. Geoms
are stateless value objects with class-based equality and hashing.

``lets_plot_aes`` builds a layer's positional/non-positional aesthetic mapping.
Collective grouping (the ``collect by`` clause, ``group_aes_cols``) belongs to a
later rendering PR and is not defined here yet.
"""

from __future__ import annotations

import lets_plot

from ..constants import BLANK_AES_COLUMN, POLAR_TO_CART_AES
from .utils import mapping_col_name


class SglGeom:
    def geom_name(self) -> str:
        return "geom"

    def is_collective(self) -> bool:
        return False

    def lets_plot_aes_args(self, layer: dict, df, scales: dict) -> dict[str, str]:
        """The ``{aesthetic: column}`` args for this layer's lets-plot mapping.

        Each mapped aesthetic points at its (possibly CTA-derived) column,
        ``theta``/``r`` fold onto ``x``/``y``, and any unmapped ``x``/``y`` is
        pinned to the constant blank column that ``lets_plot_layer`` adds to the
        data. Subclasses adjust the result (e.g. bars remap ``color`` to fill).
        """
        aes_args: dict[str, str] = {}
        for aes, col_expr in layer["aes_mappings"].items():
            key = POLAR_TO_CART_AES.get(aes, aes)
            aes_args[key] = mapping_col_name(aes, col_expr, scales)
        aes_args.setdefault("x", BLANK_AES_COLUMN)
        aes_args.setdefault("y", BLANK_AES_COLUMN)
        return aes_args

    def lets_plot_aes(self, layer: dict, df, scales: dict):
        """Build the lets-plot ``aes`` mapping for this layer.

        Mirrors rsgl's ``ggplot_aes.sgl_geom``.
        """
        return lets_plot.aes(**self.lets_plot_aes_args(layer, df, scales))

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
