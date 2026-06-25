"""Resolve SGL column references against result DataFrame column names.

SGL column references are matched to their actual stored column casing
case-insensitively, so a statement like ``HP as x`` binds to an ``hp`` column.
This mirrors how SQL databases (e.g. DuckDB) treat unquoted identifiers and
removes a surprising source of "column not found" errors when the SGL casing
differs from the stored column casing.

This pass runs after the result DataFrames are fetched and rewrites aes,
grouping, collection, and facet column names to the actual stored casing before
semantic validation.
"""

from __future__ import annotations

import polars as pl


def col_has_match_in_df(col_expr: dict, df: pl.DataFrame) -> bool:
    """Whether the col_expr's column matches a df column, ignoring case."""
    return col_expr["column"].lower() in [name.lower() for name in df.columns]


def facet_has_match_in_df(facet_expr: dict, df: pl.DataFrame) -> bool:
    """Whether the facet's column matches a df column, ignoring case."""
    return facet_expr["column"].lower() in [name.lower() for name in df.columns]


def _first_matching_name(col_name: str, df: pl.DataFrame) -> str:
    """The first df column name matching col_name, ignoring case."""
    return next(name for name in df.columns if name.lower() == col_name.lower())


def match_col_to_df(col_expr: dict, df: pl.DataFrame) -> dict:
    """Rewrite the col_expr's column to its df casing if one matches."""
    if not col_has_match_in_df(col_expr, df):
        return col_expr
    return {**col_expr, "column": _first_matching_name(col_expr["column"], df)}


def match_facet_to_df(facet_expr: dict, df: pl.DataFrame) -> dict:
    """Rewrite the facet's column to its df casing."""
    return {
        **facet_expr,
        "column": _first_matching_name(facet_expr["column"], df),
    }


def match_cols_to_df(col_exprs, df: pl.DataFrame):
    """Rewrite each col_expr's column to df casing where one matches.

    Accepts either a dict of aesthetic name -> col_expr (``aes_mappings``) or a
    list of col_exprs (``groupings``/``collections``), returning the same shape.
    """
    if isinstance(col_exprs, dict):
        return {
            aesthetic: match_col_to_df(col_expr, df)
            for aesthetic, col_expr in col_exprs.items()
        }
    return [match_col_to_df(col_expr, df) for col_expr in col_exprs]


def match_col_casing_for_layer(layer: dict, df: pl.DataFrame) -> dict:
    """Rewrite a layer's aes, grouping, and collection columns to df casing."""
    matched = {**layer, "aes_mappings": match_cols_to_df(layer["aes_mappings"], df)}
    if "groupings" in matched:
        matched["groupings"] = match_cols_to_df(matched["groupings"], df)
    if "collections" in matched:
        matched["collections"] = match_cols_to_df(matched["collections"], df)
    return matched


def match_col_casing_for_facet(facet_expr: dict, dfs: list[pl.DataFrame]) -> dict:
    """Rewrite a facet's column to the casing of the first df that matches."""
    for df in dfs:
        if facet_has_match_in_df(facet_expr, df):
            return match_facet_to_df(facet_expr, df)
    return facet_expr


def match_col_casing_for_layers(
    layers: list[dict], dfs: list[pl.DataFrame]
) -> list[dict]:
    """Rewrite each layer's columns to the casing of its own data source."""
    return [
        match_col_casing_for_layer(layer, df)
        for layer, df in zip(layers, dfs)
    ]


def match_col_casing_for_facets(
    facets: list[dict], dfs: list[pl.DataFrame]
) -> list[dict]:
    """Rewrite each facet's column to the casing of a matching data source."""
    return [match_col_casing_for_facet(facet, dfs) for facet in facets]


def match_col_casing(pgs: dict, dfs: list[pl.DataFrame]) -> dict:
    """Rewrite all column references in the pgs to their stored df casing."""
    matched = {**pgs, "layers": match_col_casing_for_layers(pgs["layers"], dfs)}
    if "facets" in matched:
        matched["facets"] = match_col_casing_for_facets(matched["facets"], dfs)
    return matched
