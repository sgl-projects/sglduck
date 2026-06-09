"""The line geom."""

from __future__ import annotations

import plotnine

from .base import SglGeom


class SglGeomLine(SglGeom):
    def geom_name(self) -> str:
        return "line"

    def is_collective(self) -> bool:
        return True

    def has_direction(self) -> bool:
        return True

    def plotnine_geom(self):
        return plotnine.geom_line
