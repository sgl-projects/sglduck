"""The avg aggregation CTA."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from .base import Aggregation, SglCta
from .utils import raise_if_arg_present


class SglCtaAvg(SglCta):
    def sgl_func_name(self) -> str:
        return "avg"

    def valid_cta(self, col_expr: dict, df: pd.DataFrame) -> None:
        # sglduck.types imports sglduck.cta (via sglduck.utils), so import lazily
        from ..types import is_numerical_col

        col_name = col_expr["column"]
        avg_fn_name = self.sgl_func_name()
        if col_name == "*":
            raise SglError("Error: '*' cannot be used with the avg function.")

        if not is_numerical_col(df[col_name]):
            raise SglError(
                f"Error: {avg_fn_name} function can only be applied to"
                " numerical columns."
            )

        raise_if_arg_present(col_expr)

    def is_aggregation(self) -> bool:
        return True

    def is_transformation(self) -> bool:
        return False

    def needs_scaling(self) -> bool:
        return True

    def agg_col_name(self, col_expr: dict, scale) -> str:
        scale_nm = "linear" if scale is None else scale.sgl_func_name()
        return f"sglduck.{scale_nm}.{self.sgl_func_name()}.{col_expr['column']}"

    def agg_col_expr(self, col_expr: dict, scale) -> Aggregation:
        if scale is None:
            column = col_expr["column"]
        else:
            column = f"sglduck.{scale.sgl_func_name()}.{col_expr['column']}"
        return Aggregation("mean", column)

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.sgl_func_name()}({col_expr['column']})"
