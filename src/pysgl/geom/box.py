"""The box geom."""

from __future__ import annotations

from .base import SglGeom


class SglGeomBox(SglGeom):
    def geom_name(self) -> str:
        return "box"

    def is_collective(self) -> bool:
        return True

    def has_direction(self) -> bool:
        return True

    def plotnine_geom(self):
        import plotnine

        return plotnine.geom_boxplot
