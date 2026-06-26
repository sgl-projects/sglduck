"""The line geom."""

from __future__ import annotations

import lets_plot

from .base import SglGeom
from .utils import mapping_col_name


class SglGeomLine(SglGeom):
    def geom_name(self) -> str:
        return "line"

    def valid_qual_list(self) -> list[str]:
        return ["horizontal", "regression", "vertical"]

    def valid_non_pos_aes(self) -> list[str]:
        return ["color"]

    def is_collective(self) -> bool:
        return True

    def extension(self) -> int:
        return 2

    def has_direction(self) -> bool:
        return True

    def lets_plot_dir_from_qual(self, qual: str) -> str:
        return "x" if qual == "horizontal" else "y"

    def default_group_cols(self, layer: dict, df, scales: dict) -> list[str]:
        # A line collects by its color aesthetic, so each colour is a separate
        # line. Mirrors rsgl's group_aes_cols.sgl_geom_line.
        aes_mappings = layer["aes_mappings"]
        if "color" in aes_mappings:
            return [mapping_col_name("color", aes_mappings["color"], scales)]
        return []

    def lets_plot_geom(self):
        return lets_plot.geom_line
