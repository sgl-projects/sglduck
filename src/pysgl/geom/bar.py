"""The bar geom."""

from __future__ import annotations

import plotnine

from .base import SglGeom


class SglGeomBar(SglGeom):
    def geom_name(self) -> str:
        return "bar"

    def has_direction(self) -> bool:
        return True

    def plotnine_geom(self):
        return plotnine.geom_bar
