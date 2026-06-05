"""Base class for SGL geoms (~ R/sgl_geom.R).

As with CTAs, rsgl represents a geom as an empty, S3-classed list and dispatches
behaviour through generics; here each generic becomes a method. Geoms are
stateless value objects with class-based equality and hashing.

Methods that require a layer, DataFrame or scales (``plotnine_aes``,
``group_aes_cols``) belong to the rendering milestone and are not defined here
yet.
"""

from __future__ import annotations


class SglGeom:
    def geom_name(self) -> str:
        return "geom"

    def is_collective(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
