"""The bar geom."""

from __future__ import annotations

import lets_plot

from .base import SglGeom


class SglGeomBar(SglGeom):
    def geom_name(self) -> str:
        return "bar"

    def valid_qual_list(self) -> list[str]:
        return ["horizontal", "unstacked", "vertical"]

    def valid_non_pos_aes(self) -> list[str]:
        return ["color"]

    def has_direction(self) -> bool:
        return True

    def lets_plot_dir_from_qual(self, qual: str) -> str:
        return "x" if qual == "vertical" else "y"

    def lets_plot_aes_args(self, layer: dict, df, scales: dict) -> dict[str, str]:
        # A bar colours its interior, so the color aesthetic maps onto fill
        # rather than the default stroke. Mirrors rsgl's ggplot_aes.sgl_geom_bar.
        aes_args = super().lets_plot_aes_args(layer, df, scales)
        if "color" in aes_args:
            aes_args["fill"] = aes_args.pop("color")
        return aes_args

    def lets_plot_geom(self):
        return lets_plot.geom_bar
