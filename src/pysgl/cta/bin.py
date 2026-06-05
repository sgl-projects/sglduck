"""The bin transformation CTA (~ R/sgl_cta_bin.R)."""

from __future__ import annotations

from .base import SglCta


class SglCtaBin(SglCta):
    def cta_fn_name(self) -> str:
        return "bin"

    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        fn_name = self.cta_fn_name()
        if "arg" in col_expr:
            return f"{fn_name}({col_expr['column']}, {col_expr['arg']})"
        return f"{fn_name}({col_expr['column']})"
