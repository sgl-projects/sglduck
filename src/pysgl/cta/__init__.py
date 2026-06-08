"""SGL column transformations and aggregations (CTAs).

``SglCta`` is the base class; one subclass per CTA variant (identity, avg,
count, bin).
"""

from .avg import SglCtaAvg
from .base import SglCta
from .bin import SglCtaBin
from .count import SglCtaCount
from .identity import SglCtaIdentity

__all__ = [
    "SglCta",
    "SglCtaIdentity",
    "SglCtaAvg",
    "SglCtaCount",
    "SglCtaBin",
]
