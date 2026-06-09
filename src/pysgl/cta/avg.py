"""The avg aggregation CTA."""

from __future__ import annotations

from .base import SglCta


class SglCtaAvg(SglCta):
    def sgl_func_name(self) -> str:
        return "avg"

    def is_aggregation(self) -> bool:
        return True

    def is_transformation(self) -> bool:
        return False

    def needs_scaling(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.sgl_func_name()}({col_expr['column']})"
