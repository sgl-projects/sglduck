"""The box geom."""

from __future__ import annotations

import lets_plot

from .base import SglGeom


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

    def lets_plot_geom(self):
        return lets_plot.geom_boxplot
