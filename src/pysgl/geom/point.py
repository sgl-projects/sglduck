"""The point geom."""

from __future__ import annotations

import plotnine

from .base import SglGeom


class SglGeomPoint(SglGeom):
    def geom_name(self) -> str:
        return "point"

    def has_direction(self) -> bool:
        return False

    def plotnine_geom(self):
        return plotnine.geom_point
