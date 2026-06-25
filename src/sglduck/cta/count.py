"""The count aggregation CTA."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from .base import Aggregation, SglCta
from .utils import raise_if_arg_present


class SglCtaCount(SglCta):
    def sgl_func_name(self) -> str:
        return "count"

    def valid_cta(self, col_expr: dict, df: pd.DataFrame) -> None:
        count_fn_name = self.sgl_func_name()
        col_name = col_expr["column"]
        if col_name != "*":
            raise SglError(
                f"Error: {count_fn_name} can only be applied to *,"
                f" found {count_fn_name}({col_name})."
            )

        raise_if_arg_present(col_expr)

    def is_aggregation(self) -> bool:
        return True

    def is_transformation(self) -> bool:
        return False

    def needs_scaling(self) -> bool:
        return False

    def agg_col_name(self, col_expr: dict, scale) -> str:
        return "sglduck.count"

    def agg_col_expr(self, col_expr: dict, scale) -> Aggregation:
        return Aggregation("size", None)

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.sgl_func_name()}(*)"
