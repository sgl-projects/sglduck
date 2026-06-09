"""Base class for SGL scales.

As with geoms and CTAs, a scale's behaviour lives in methods on the class
hierarchy. Scales are stateless value objects with class-based equality and
hashing.

Methods that require layers, DataFrames or the full grammar structure
(``valid_scale``, ``plotnine_scales``) belong to the validation and rendering
milestones and are not defined here yet.
"""

from __future__ import annotations


class SglScale:
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
