"""The point geom (~ R/sgl_geom_point.R)."""

from __future__ import annotations

from .base import SglGeom


class SglGeomPoint(SglGeom):
    def geom_name(self) -> str:
        return "point"

    def has_direction(self) -> bool:
        return False

    def plotnine_geom(self):
        import plotnine

        return plotnine.geom_point
