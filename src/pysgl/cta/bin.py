"""The bin transformation CTA."""

from __future__ import annotations

from .base import SglCta


class SglCtaBin(SglCta):
    def sgl_func_name(self) -> str:
        return "bin"

    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        fn_name = self.sgl_func_name()
        if "arg" in col_expr:
            return f"{fn_name}({col_expr['column']}, {col_expr['arg']})"
        return f"{fn_name}({col_expr['column']})"
