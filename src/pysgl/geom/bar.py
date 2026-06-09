"""The bar geom."""

from __future__ import annotations

from .base import SglGeom


class SglGeomBar(SglGeom):
    def geom_name(self) -> str:
        return "bar"

    def has_direction(self) -> bool:
        return True

    def plotnine_geom(self):
        import plotnine

        return plotnine.geom_bar
