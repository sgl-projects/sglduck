"""Base class for SGL CTAs.

A CTA's behaviour lives in methods on the class hierarchy. CTAs are stateless
value objects, so two instances of the same class compare equal and hash alike;
this lets groupings and collections be de-duplicated by value.

Methods that require a layer or scales (``add_transformed_column``,
``agg_col_name``, ``agg_col_expr``) belong to the data-pipeline milestone and
are intentionally not defined here yet.
"""

from __future__ import annotations


class SglCta:
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
