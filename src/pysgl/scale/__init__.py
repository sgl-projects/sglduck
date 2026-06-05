"""SGL scales.

Mirrors rsgl's ``R/sgl_scale*.R``. ``SglScale`` is the base class; one subclass
per scale variant (linear, log, ln), matching rsgl's S3 hierarchy.
"""

from .base import SglScale
from .linear import SglScaleLinear
from .ln import SglScaleLn
from .log import SglScaleLog

__all__ = [
    "SglScale",
    "SglScaleLinear",
    "SglScaleLog",
    "SglScaleLn",
]
