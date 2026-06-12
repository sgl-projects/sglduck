"""The bin transformation CTA."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from .base import SglCta


class SglCtaBin(SglCta):
    def sgl_func_name(self) -> str:
        return "bin"

    def valid_cta(self, col_expr: dict, df: pd.DataFrame) -> None:
        # pysgl.types imports pysgl.cta (via pysgl.utils), so import lazily
        from ..types import is_categorical_col

        col_name = col_expr["column"]
        if col_name == "*":
            raise SglError(
                "Error: '*' can only be used inside an aggregation function"
            )
        if is_categorical_col(df[col_name]):
            bin_fn_name = self.sgl_func_name()
            raise SglError(
                f"Error: cannot apply {bin_fn_name} to a categorical column,"
                f" found {bin_fn_name}({col_name})."
            )

        if "arg" in col_expr and col_expr["arg"] <= 0:
            raise SglError("Error: number of bins must be greater than 0.")

    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        fn_name = self.sgl_func_name()
        if "arg" in col_expr:
            return f"{fn_name}({col_expr['column']}, {col_expr['arg']})"
        return f"{fn_name}({col_expr['column']})"
