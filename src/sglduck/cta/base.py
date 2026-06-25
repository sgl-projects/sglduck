"""Base class for SGL CTAs.

A CTA's behaviour lives in methods on the class hierarchy. CTAs are stateless
value objects, so two instances of the same class compare equal and hash alike;
this lets groupings and collections be de-duplicated by value.

The transform/aggregate generics (``add_transformed_column``, ``agg_col_name``,
``agg_col_expr``) live on the variants that support them rather than on the base
class, mirroring rsgl's S3 methods.
"""

from __future__ import annotations

from typing import NamedTuple


class Aggregation(NamedTuple):
    """A pandas-side aggregation spec, the analog of rsgl's quoted dplyr expr.

    ``func`` is ``"mean"`` or ``"size"``; ``column`` is the source column to
    aggregate (``None`` for ``"size"``, which counts rows).
    """

    func: str
    column: str | None


class SglCta:
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
