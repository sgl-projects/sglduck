"""SGL type classification of dataframe columns and aes mappings.

Columns classify as numerical, categorical, or temporal, with temporal split
into dates and timestamps for the date-vs-timestamp reconciliation in
``cast_columns``. polars carries first-class dtypes, so classification is a
direct dispatch on a column's dtype, mirroring rsgl's ``class(col)[1]`` checks:
DATE columns are ``pl.Date`` and TIMESTAMP columns are ``pl.Datetime``.
"""

from __future__ import annotations

import polars as pl

from .result_dfs import _query
from .utils import col_expr_has_cta


def is_numerical_col(col: pl.Series) -> bool:
    """Whether the column is numerical (ints, floats, decimals, or durations)."""
    return col.dtype.is_numeric() or col.dtype == pl.Duration


def is_categorical_col(col: pl.Series) -> bool:
    """Whether the column is categorical (booleans, strings, or categories)."""
    return col.dtype in (pl.Boolean, pl.String, pl.Categorical, pl.Enum)


def is_date_col(col: pl.Series) -> bool:
    """Whether the column holds calendar dates without a time component."""
    return col.dtype == pl.Date


def is_timestamp_col(col: pl.Series) -> bool:
    """Whether the column holds timestamps (instants with a time component)."""
    return col.dtype == pl.Datetime


def is_temporal_col(col: pl.Series) -> bool:
    """Whether the column is temporal (a date or a timestamp)."""
    return is_date_col(col) or is_timestamp_col(col)


def _mapped_column(layer: dict, df: pl.DataFrame, aes: str) -> pl.Series | None:
    """The df column the aesthetic maps to, or ``None`` when it isn't in the frame.

    A binned or aggregated mapping's source column does not survive
    ``perform_ctas`` (it is consumed by the bin/aggregation), so an orientation
    type check can run against a frame that no longer has it. rsgl relies on R
    returning ``NULL`` for a missing column — the type checks then read as
    ``FALSE`` — whereas polars raises, so the absence is made explicit here.
    """
    column = layer["aes_mappings"][aes]["column"]
    return df[column] if column in df.columns else None


def is_numerical_mapping(layer: dict, df: pl.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is numerical."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return True
    col = _mapped_column(layer, df, aes)
    return col is not None and is_numerical_col(col)


def is_categorical_mapping(layer: dict, df: pl.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is categorical."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    col = _mapped_column(layer, df, aes)
    return col is not None and is_categorical_col(col)


def is_date_mapping(layer: dict, df: pl.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is a date."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    col = _mapped_column(layer, df, aes)
    return col is not None and is_date_col(col)


def is_timestamp_mapping(layer: dict, df: pl.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is a timestamp."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    col = _mapped_column(layer, df, aes)
    return col is not None and is_timestamp_col(col)


def is_temporal_mapping(layer: dict, df: pl.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is temporal."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    return is_date_mapping(layer, df, aes) or is_timestamp_mapping(layer, df, aes)


def is_binned_mapping(layer: dict, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is binned."""
    aes_mapping = layer["aes_mappings"][aes]
    return col_expr_has_cta(aes_mapping, "bin")


def type_classifications(con, table_name: str):
    """Get SGL type classifications for columns in a table.

    ``type_classifications`` takes a database connection and a table name
    and returns the SGL type classifications (numerical, categorical, or
    temporal) of the table's columns.

    Classification is driven by each column's polars dtype, which DuckDB
    supplies from the table schema regardless of row count.

    :param con: A DuckDB connection.
    :param table_name: The name of a table.
    :return: A dataframe listing the SGL type classification of each column.
    """
    sql = f"select * from {_quote_identifier(table_name)} limit 1"
    df = _query(con, sql)

    def col_class(col: pl.Series) -> str:
        if is_numerical_col(col):
            return "numerical"
        if is_categorical_col(col):
            return "categorical"
        if is_temporal_col(col):
            return "temporal"
        return "unknown"

    return pl.DataFrame(
        {
            "column_name": list(df.columns),
            "column_class": [col_class(df[name]) for name in df.columns],
        }
    )


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'
