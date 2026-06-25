"""Base class for SGL scales.

As with geoms and CTAs, a scale's behaviour lives in methods on the class
hierarchy. Scales are stateless value objects with class-based equality and
hashing.

``lets_plot_scales`` requires the full grammar structure and belongs to the
rendering milestone, so it is not defined here yet.
"""

from __future__ import annotations

from ..errors import SglError


class SglScale:
    def valid_scale(self, aes: str, layers: list[dict], dfs) -> None:
        all_mapped_aes = {
            mapped_aes for layer in layers for mapped_aes in layer["aes_mappings"]
        }
        if aes not in all_mapped_aes:
            raise SglError("Error: a scaled aesthetic must have at least one mapping")

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
