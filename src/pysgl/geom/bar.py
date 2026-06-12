"""The bar geom."""

from __future__ import annotations

import plotnine

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

    def plotnine_geom(self):
        return plotnine.geom_bar
