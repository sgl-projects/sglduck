"""The avg aggregation CTA (~ R/sgl_cta_avg.R)."""

from __future__ import annotations

from .base import SglCta


class SglCtaAvg(SglCta):
    def cta_fn_name(self) -> str:
        return "avg"

    def is_aggregation(self) -> bool:
        return True

    def is_transformation(self) -> bool:
        return False

    def needs_scaling(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.cta_fn_name()}({col_expr['column']})"
