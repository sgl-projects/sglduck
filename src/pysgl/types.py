"""SGL type classification of dataframe columns and aes mappings.

Columns classify as numerical, categorical, or temporal, with temporal split
into dates and timestamps for the date-vs-timestamp reconciliation in
``cast_columns``. pandas has no first-class pure-date dtype — DB drivers
return DATE columns as object-dtype ``datetime.date`` values and TIMESTAMP
columns as ``datetime64`` — so the helpers inspect element types as well as
dtypes.
"""

from __future__ import annotations

import datetime

import pandas as pd
import pandas.api.types as pdt

from .result_dfs import _query
from .utils import col_expr_has_cta, column_from_aes


def is_numerical_col(col: pd.Series) -> bool:
    """Whether the column is numerical (ints, floats, or timedeltas)."""
    if pdt.is_bool_dtype(col.dtype):
        return False
    return pdt.is_numeric_dtype(col.dtype) or pdt.is_timedelta64_dtype(col.dtype)


def is_categorical_col(col: pd.Series) -> bool:
    """Whether the column is categorical (booleans, strings, or categories)."""
    if pdt.is_bool_dtype(col.dtype) or isinstance(col.dtype, pd.CategoricalDtype):
        return True
    if pdt.is_object_dtype(col.dtype):
        return isinstance(_first_valid_element(col), str)
    return pdt.is_string_dtype(col.dtype)


def is_date_col(col: pd.Series) -> bool:
    """Whether the column holds calendar dates without a time component."""
    if not pdt.is_object_dtype(col.dtype):
        return False
    element = _first_valid_element(col)
    return isinstance(element, datetime.date) and not isinstance(
        element, datetime.datetime
    )


def is_timestamp_col(col: pd.Series) -> bool:
    """Whether the column holds timestamps (instants with a time component)."""
    if pdt.is_datetime64_any_dtype(col.dtype):
        return True
    if pdt.is_object_dtype(col.dtype):
        return isinstance(_first_valid_element(col), datetime.datetime)
    return False


def is_temporal_col(col: pd.Series) -> bool:
    """Whether the column is temporal (a date or a timestamp)."""
    return is_date_col(col) or is_timestamp_col(col)


def is_numerical_mapping(layer: dict, df: pd.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is numerical."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return True
    return is_numerical_col(column_from_aes(layer, df, aes))


def is_categorical_mapping(layer: dict, df: pd.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is categorical."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    return is_categorical_col(column_from_aes(layer, df, aes))


def is_date_mapping(layer: dict, df: pd.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is a date."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    return is_date_col(column_from_aes(layer, df, aes))


def is_timestamp_mapping(layer: dict, df: pd.DataFrame, aes: str) -> bool:
    """Whether the layer's mapping to the aesthetic is a timestamp."""
    aes_mapping = layer["aes_mappings"][aes]
    if col_expr_has_cta(aes_mapping, "count"):
        return False
    return is_timestamp_col(column_from_aes(layer, df, aes))


def is_temporal_mapping(layer: dict, df: pd.DataFrame, aes: str) -> bool:
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

    Classification samples one row from the table, so columns of a table
    with no rows classify as "unknown".

    :param con: A database connection (anything ``pandas.read_sql_query``
        accepts — a SQLAlchemy connectable or any DB-API 2.0 connection).
    :param table_name: The name of a table.
    :return: A dataframe listing the SGL type classification of each column.
    """
    sql = f"select * from {_quote_identifier(table_name)} limit 1"
    df = _query(con, sql)

    def col_class(col: pd.Series) -> str:
        if is_numerical_col(col):
            return "numerical"
        if is_categorical_col(col):
            return "categorical"
        if is_temporal_col(col):
            return "temporal"
        return "unknown"

    return pd.DataFrame(
        {
            "column_name": list(df.columns),
            "column_class": [col_class(df[name]) for name in df.columns],
        }
    )


def _first_valid_element(col: pd.Series):
    non_null = col.dropna()
    return non_null.iloc[0] if len(non_null) else None


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'
