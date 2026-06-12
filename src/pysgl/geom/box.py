"""The box geom."""

from __future__ import annotations

import plotnine

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

    def has_direction(self) -> bool:
        return True

    def plotnine_geom(self):
        return plotnine.geom_boxplot
