"""SGL scales.

``SglScale`` is the base class; one subclass per scale variant (linear, log,
ln).
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
