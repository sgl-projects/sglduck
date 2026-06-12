"""The line geom."""

from __future__ import annotations

import plotnine

from .base import SglGeom


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

    def plotnine_geom(self):
        return plotnine.geom_line
