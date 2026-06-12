"""Validate that referenced columns exist in the layer's data source."""

from __future__ import annotations

import pandas as pd

from ..errors import SglError


def column_exists(col_exprs: list[dict], df: pd.DataFrame) -> dict[str, bool]:
    """Map each unique referenced column to whether it exists in the df."""
    refs = dict.fromkeys(col_expr["column"] for col_expr in col_exprs)
    results = {ref: ref in df.columns for ref in refs}
    if "*" in results:
        results["*"] = True
    return results


def raise_if_col_missing(col_exprs: list[dict], df: pd.DataFrame) -> None:
    """Raise if any of the col_exprs reference a column the df lacks."""
    exists_results = column_exists(col_exprs, df)
    missing_col_names = [
        col_name for col_name, exists in exists_results.items() if not exists
    ]
    if missing_col_names:
        raise SglError(
            f"Error: referenced column '{missing_col_names[0]}' not found"
        )


def valid_column_refs(layer: dict, df: pd.DataFrame) -> None:
    """Raise if any clause of the layer references a missing column."""
    for col_exprs in (
        list(layer["aes_mappings"].values()),
        layer.get("groupings", []),
        layer.get("collections", []),
    ):
        raise_if_col_missing(col_exprs, df)
