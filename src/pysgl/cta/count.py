"""The count aggregation CTA (~ R/sgl_cta_count.R)."""

from __future__ import annotations

from .base import SglCta


class SglCtaCount(SglCta):
    def sgl_func_name(self) -> str:
        return "count"

    def is_aggregation(self) -> bool:
        return True

    def is_transformation(self) -> bool:
        return False

    def needs_scaling(self) -> bool:
        return False

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.sgl_func_name()}(*)"
