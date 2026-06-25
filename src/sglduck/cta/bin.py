"""The bin transformation CTA."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError
from .base import SglCta
from .bin_utils import bin_values


class SglCtaBin(SglCta):
    def sgl_func_name(self) -> str:
        return "bin"

    def valid_cta(self, col_expr: dict, df: pd.DataFrame) -> None:
        # sglduck.types imports sglduck.cta (via sglduck.utils), so import lazily
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

    def add_transformed_column(
        self, input_col_name: str, df: pd.DataFrame, scale, num_bins: int = 30
    ) -> pd.DataFrame:
        """Return ``df`` with a binned column for ``input_col_name`` added.

        The new column is named ``sglduck.<scale>.bin.<num_bins>.<column>``; if a
        column by that name already exists the frame is returned unchanged, so
        the same (column, scale, bin-count) transform is never duplicated.
        """
        new_col_name = (
            f"sglduck.{scale.sgl_func_name()}.{self.sgl_func_name()}"
            f".{num_bins}.{input_col_name}"
        )
        if new_col_name in df.columns:
            return df
        df = df.copy()
        df[new_col_name] = bin_values(df[input_col_name], num_bins, scale)
        return df

    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return True

    def expr_text(self, col_expr: dict) -> str:
        fn_name = self.sgl_func_name()
        if "arg" in col_expr:
            return f"{fn_name}({col_expr['column']}, {col_expr['arg']})"
        return f"{fn_name}({col_expr['column']})"
