"""Base class for SGL geoms.

As with CTAs, a geom's behaviour lives in methods on the class hierarchy. Geoms
are stateless value objects with class-based equality and hashing.

``lets_plot_aes_args`` builds a layer's positional/non-positional aesthetic
mapping; ``group_cols`` resolves how the layer splits into collective groups.
``lets_plot_layer`` (in ``rgs_to_lets_plot``) assembles these into the geom.
"""

from __future__ import annotations

from ..constants import BLANK_AES_COLUMN, POLAR_TO_CART_AES
from .utils import collection_group_cols, mapping_col_name


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

    def group_cols(self, layer: dict, df, scales: dict) -> list[str]:
        """The df columns the layer splits into separate groups by.

        An explicit ``collect by`` clause takes precedence; otherwise a geom may
        define a default collection (see ``default_group_cols``). Mirrors rsgl's
        collections handling plus the per-geom ``group_aes_cols``.
        """
        collected = collection_group_cols(layer, scales)
        if collected:
            return collected
        return self.default_group_cols(layer, df, scales)

    def default_group_cols(self, layer: dict, df, scales: dict) -> list[str]:
        """The geom's default grouping columns (none for non-collective geoms)."""
        return []

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
