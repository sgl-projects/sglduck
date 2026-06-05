"""Base class for SGL CTAs (~ R/sgl_cta.R).

In rsgl a CTA is an empty, S3-classed list and its behaviour lives in
single-dispatch generics (``R/generics.R``); here each generic becomes a method
on the class hierarchy. CTAs are stateless value objects, so two instances of
the same class compare equal and hash alike — mirroring rsgl's reliance on
``identical()`` and ``%in%`` to de-duplicate groupings/collections.

Methods that require a DataFrame, layer or scales (``valid_cta``,
``add_transformed_column``, ``agg_col_name``, ``agg_col_expr``) belong to the
validation and data-pipeline milestones and are intentionally not defined here
yet.
"""

from __future__ import annotations


class SglCta:
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other)

    def __hash__(self) -> int:
        return hash(type(self))

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
