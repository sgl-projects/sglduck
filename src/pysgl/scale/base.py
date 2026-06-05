"""Base class for SGL scales (~ R/sgl_scale.R).

As with geoms and CTAs, rsgl represents a scale as an empty, S3-classed list and
dispatches behaviour through generics; here each generic becomes a method.
Scales are stateless value objects with class-based equality and hashing.

Methods that require layers, DataFrames or the full grammar structure
(``valid_scale``, ``plotnine_scales``) belong to the validation and rendering
milestones and are not defined here yet.
"""

from __future__ import annotations


class SglScale:
    def scale_name(self) -> str:
        return "base"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
