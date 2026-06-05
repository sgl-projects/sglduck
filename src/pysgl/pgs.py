"""Reconstruct the typed "pgs" object graph from the C bridge output.

The compiled bridge (``pysgl._sgl.sgl_to_pgs``) returns the pgs as plain Python
containers, carrying geom/cta/scale variants as ``{"class": "sgl_..."}`` string
tags — exactly where rsgl's Rcpp bridge set the S3 ``class`` attribute. This
module walks that structure and swaps each class-tagged dict for the
corresponding typed object (``SglGeom*`` / ``SglCta*`` / ``SglScale*``), leaving
the surrounding lists/dicts untouched. The result mirrors rsgl's ``rgs``: a
nested structure whose geom/cta/scale leaves are classed value objects.

``sgl_to_pgs`` is the Python-side analog of rsgl's ``sgl_to_rgs`` (which in R is
the Rcpp function itself, since Rcpp sets the classes inline).
"""

from __future__ import annotations

from . import _sgl
from .cta import SglCtaAvg, SglCtaBin, SglCtaCount, SglCtaIdentity
from .geom import SglGeomBar, SglGeomBox, SglGeomLine, SglGeomPoint
from .scale import SglScaleLinear, SglScaleLn, SglScaleLog

_CLASS_REGISTRY = {
    "sgl_geom_point": SglGeomPoint,
    "sgl_geom_bar": SglGeomBar,
    "sgl_geom_line": SglGeomLine,
    "sgl_geom_box": SglGeomBox,
    "sgl_cta_identity": SglCtaIdentity,
    "sgl_cta_avg": SglCtaAvg,
    "sgl_cta_count": SglCtaCount,
    "sgl_cta_bin": SglCtaBin,
    "sgl_scale_linear": SglScaleLinear,
    "sgl_scale_log": SglScaleLog,
    "sgl_scale_ln": SglScaleLn,
}


def _reconstruct(node):
    if isinstance(node, dict):
        class_tag = node.get("class")
        if class_tag in _CLASS_REGISTRY:
            return _CLASS_REGISTRY[class_tag]()
        return {key: _reconstruct(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_reconstruct(item) for item in node]
    return node


def reconstruct_pgs(raw_pgs: dict) -> dict:
    """Replace class-tagged dicts in a raw bridge pgs with typed objects."""
    return _reconstruct(raw_pgs)


def sgl_to_pgs(sgl_stmt: str) -> dict:
    """Parse a SGL statement into the typed pgs object graph."""
    return reconstruct_pgs(_sgl.sgl_to_pgs(sgl_stmt))
