"""Validate the pgs facets against the layer data sources."""

from __future__ import annotations

import polars as pl

from ..errors import SglError
from ..types import is_categorical_col, is_numerical_col, is_temporal_col


def in_at_least_one_data_source(col_name: str, dfs: list[pl.DataFrame]) -> bool:
    """Whether any layer data source has the column."""
    return any(col_name in df.columns for df in dfs)


def col_type(col_name: str, df: pl.DataFrame) -> str | None:
    """The column's SGL type classification, or None if the df lacks it."""
    if col_name not in df.columns:
        return None
    col = df[col_name]
    if is_categorical_col(col):
        return "categorical"
    if is_numerical_col(col):
        return "numerical"
    if is_temporal_col(col):
        return "temporal"
    return "unknown"


def all_types(col_name: str, dfs: list[pl.DataFrame]) -> list[str]:
    """The unique classifications of the column across the data sources."""
    types = (col_type(col_name, df) for df in dfs)
    return list(dict.fromkeys(t for t in types if t is not None))


def valid_facet(pgs: dict, dfs: list[pl.DataFrame]) -> None:
    """Raise if the pgs facets are invalid."""
    if "facets" not in pgs:
        return
    facets = pgs["facets"]
    if len(facets) > 2:
        raise SglError("Error: cannot have more than two facets.")
    if len(facets) == 2:
        facet_directions = [facet["direction"] for facet in facets]
        if all(direction == "vertical" for direction in facet_directions) or all(
            direction == "horizontal" for direction in facet_directions
        ):
            raise SglError(
                "Error: for two facets, one must be horizontal and the other"
                " vertical."
            )
    facet_col_names = [facet["column"] for facet in facets]
    missing_cols = [
        col_name
        for col_name in facet_col_names
        if not in_at_least_one_data_source(col_name, dfs)
    ]
    if missing_cols:
        raise SglError(
            f"Error: facet column '{missing_cols[0]}' does not exist in any"
            " layer data sources."
        )
    for facet_col in facet_col_names:
        facet_col_types = all_types(facet_col, dfs)
        if "unknown" in facet_col_types:
            raise SglError(
                "Error: unknown SGL type classification"
                " (numerical, categorical, or temporal)"
                f" for column '{facet_col}'."
            )
        if len(facet_col_types) > 1:
            raise SglError(
                f"Error: facet column '{facet_col}' does not have a consistent"
                " type (categorical, numerical, or temporal) across"
                " all layers where it is present."
            )
