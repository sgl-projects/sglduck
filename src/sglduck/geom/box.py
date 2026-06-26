"""The box geom."""

from __future__ import annotations

import lets_plot

from ..constants import CART_AES, POS_AES
from .base import SglGeom
from .utils import mapping_col_name


class SglGeomBox(SglGeom):
    def geom_name(self) -> str:
        return "box"

    def valid_qual_list(self) -> list[str]:
        return ["horizontal", "vertical"]

    def valid_non_pos_aes(self) -> list[str]:
        return ["color"]

    def is_collective(self) -> bool:
        return True

    def extension(self) -> int:
        return 1

    def has_direction(self) -> bool:
        return True

    def lets_plot_dir_from_qual(self, qual: str) -> str:
        return "x" if qual == "vertical" else "y"

    def default_group_cols(self, layer: dict, df, scales: dict) -> list[str]:
        # A box collects by its category (the non-value positional axis) and by
        # color. Mirrors rsgl's group_aes_cols.sgl_geom_box. Imported lazily to
        # avoid a geom <-> lets_plot_direction import cycle.
        from ..lets_plot_direction import lets_plot_direction

        aes_mappings = layer["aes_mappings"]
        pos_mappings = {
            aes: col_expr
            for aes, col_expr in aes_mappings.items()
            if aes in POS_AES
        }
        group_cols: list[str] = []
        if len(pos_mappings) == 2:
            qual = layer["geom_expr"]["qual"]
            first_is_cart = next(iter(pos_mappings)) in CART_AES
            if qual in ("horizontal", "vertical"):
                if first_is_cart:
                    group_aes = "y" if qual == "horizontal" else "x"
                else:
                    group_aes = "r" if qual == "horizontal" else "theta"
            else:
                orientation = lets_plot_direction(layer, df)
                if first_is_cart:
                    group_aes = orientation
                else:
                    group_aes = "theta" if orientation == "x" else "r"
            group_cols.append(
                mapping_col_name(group_aes, pos_mappings[group_aes], scales)
            )
        if "color" in aes_mappings:
            group_cols.append(
                mapping_col_name("color", aes_mappings["color"], scales)
            )
        return list(dict.fromkeys(group_cols))

    def lets_plot_geom(self):
        return lets_plot.geom_boxplot
