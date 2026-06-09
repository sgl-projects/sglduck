"""The identity CTA."""

from __future__ import annotations

from .base import SglCta


class SglCtaIdentity(SglCta):
    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return False

    def expr_text(self, col_expr: dict) -> str:
        return col_expr["column"]
