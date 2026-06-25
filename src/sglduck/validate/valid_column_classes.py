"""Validate that referenced columns have a known SGL type classification."""

from __future__ import annotations

import polars as pl

from ..errors import SglError
from ..types import is_categorical_col, is_numerical_col, is_temporal_col


def valid_column_class(column: str, df: pl.DataFrame) -> None:
    """Raise if the column's SGL type classification is unknown."""
    if column == "*":
        return
    col = df[column]
    if is_numerical_col(col) or is_categorical_col(col) or is_temporal_col(col):
        return
    raise SglError(
        "Error: unknown SGL type classification"
        " (numerical, categorical, or temporal)"
        f" for column '{column}'."
    )


def valid_column_classes(layer: dict, df: pl.DataFrame) -> None:
    """Raise if any column referenced by the layer has an unknown class."""
    all_col_exprs = [
        *layer["aes_mappings"].values(),
        *layer.get("groupings", []),
        *layer.get("collections", []),
    ]
    for col_expr in all_col_exprs:
        valid_column_class(col_expr["column"], df)
