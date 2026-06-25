"""Run each layer's source SQL query into a pandas DataFrame.

Maps each pgs layer to the DataFrame produced by executing its
``source_sql_query`` against the supplied DuckDB connection. sglduck only
supports DuckDB connections.

Queries go through ``pandas.read_sql_query`` (DuckDB's DB-API cursor) rather
than DuckDB's native ``con.execute(sql).df()`` on purpose: the ``.df()`` path
converts DATE columns to ``datetime64``, collapsing the DATE/TIMESTAMP
distinction that the date-vs-timestamp reconciliation in ``cast_columns``
depends on. The DB-API path returns DATE columns as object-dtype
``datetime.date`` and TIMESTAMP columns as ``datetime64``, preserving it.
"""

from __future__ import annotations

import warnings

import pandas as pd


def result_dfs(pgs: dict, con) -> list[pd.DataFrame]:
    """Return one DataFrame per pgs layer, in layer order."""
    return [_query(con, layer["source_sql_query"]) for layer in pgs["layers"]]


def _query(con, sql: str) -> pd.DataFrame:
    with warnings.catch_warnings():
        # pandas warns when handed a raw DB-API connection (it only tests
        # SQLAlchemy + sqlite3), but the DuckDB DB-API path works fine —
        # suppress the cosmetic nag so it doesn't surface on every plot.
        warnings.filterwarnings(
            "ignore",
            message="pandas only supports SQLAlchemy connectable",
            category=UserWarning,
        )
        return pd.read_sql_query(sql, con)
