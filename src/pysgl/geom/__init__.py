"""SGL geoms.

Mirrors rsgl's ``R/sgl_geom*.R``. ``SglGeom`` is the base class; one subclass
per geom variant (point, bar, line, box), matching rsgl's S3 hierarchy.
"""

from .bar import SglGeomBar
from .base import SglGeom
from .box import SglGeomBox
from .line import SglGeomLine
from .point import SglGeomPoint

__all__ = [
    "SglGeom",
    "SglGeomPoint",
    "SglGeomBar",
    "SglGeomLine",
    "SglGeomBox",
]
