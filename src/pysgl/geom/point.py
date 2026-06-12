"""The point geom."""

from __future__ import annotations

import plotnine

from ..constants import NON_POS_AES
from .base import SglGeom


class SglGeomPoint(SglGeom):
    def geom_name(self) -> str:
        return "point"

    def valid_qual_list(self) -> list[str]:
        return ["jittered"]

    def valid_non_pos_aes(self) -> list[str]:
        return list(NON_POS_AES)

    def has_direction(self) -> bool:
        return False

    def plotnine_geom(self):
        return plotnine.geom_point
