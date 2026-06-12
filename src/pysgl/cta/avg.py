"""The avg aggregation CTA."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from .base import SglCta
from .utils import raise_if_arg_present


class SglCtaAvg(SglCta):
    def sgl_func_name(self) -> str:
        return "avg"

    def valid_cta(self, col_expr: dict, df: pd.DataFrame) -> None:
        # pysgl.types imports pysgl.cta (via pysgl.utils), so import lazily
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

    def expr_text(self, col_expr: dict) -> str:
        return f"{self.sgl_func_name()}({col_expr['column']})"
