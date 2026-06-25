"""Reconcile date and timestamp columns across layers before rendering.

pandas has no first-class pure-date dtype: DB drivers return DATE columns as
object-dtype ``datetime.date`` values and TIMESTAMP columns as ``datetime64``.
When a single aesthetic maps to a date in one layer and a timestamp in another,
the dates must be promoted to datetimes so the layers share a comparable axis.
``cast_columns`` finds such aesthetics and casts their date columns to
datetimes; casting a column that is already a timestamp is a no-op.
"""

from __future__ import annotations

import pandas as pd

from .types import is_date_mapping, is_timestamp_mapping
from .utils import all_aesthetics


def aes_has_dt_and_ts(aes: str, layers: list[dict], dfs: list[pd.DataFrame]) -> bool:
    """Whether the aesthetic maps to a date in some layer and a timestamp in another."""
    dt_found = False
    ts_found = False
    for layer, df in zip(layers, dfs):
        if aes in layer["aes_mappings"]:
            if is_date_mapping(layer, df, aes):
                dt_found = True
            elif is_timestamp_mapping(layer, df, aes):
                ts_found = True
    return dt_found and ts_found


def aes_with_dt_and_ts(pgs: dict, dfs: list[pd.DataFrame]) -> list[str]:
    """Return the aesthetics that map to both a date and a timestamp across layers."""
    return [
        aes
        for aes in all_aesthetics(pgs)
        if aes_has_dt_and_ts(aes, pgs["layers"], dfs)
    ]


def cast_for_aes(
    aes: str, layers: list[dict], dfs: list[pd.DataFrame]
) -> list[pd.DataFrame]:
    """Cast the aesthetic's column to a datetime in each layer that maps it.

    Layers without the aesthetic are returned unchanged; layers whose mapping
    is already a timestamp are cast too, but that cast is a no-op.
    """
    cast_dfs = []
    for layer, df in zip(layers, dfs):
        aes_mappings = layer["aes_mappings"]
        if aes not in aes_mappings:
            cast_dfs.append(df)
        else:
            col_name = aes_mappings[aes]["column"]
            cast_df = df.copy()
            cast_df[col_name] = pd.to_datetime(cast_df[col_name])
            cast_dfs.append(cast_df)
    return cast_dfs


def cast_columns(pgs: dict, dfs: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Promote dates to datetimes for aesthetics that mix dates and timestamps."""
    for aes in aes_with_dt_and_ts(pgs, dfs):
        dfs = cast_for_aes(aes, pgs["layers"], dfs)
    return dfs
