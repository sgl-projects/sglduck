"""Run each layer's source SQL query into a polars DataFrame.

Maps each pgs layer to the DataFrame produced by executing its
``source_sql_query`` against the supplied DuckDB connection. sglduck only
supports DuckDB connections.

Queries go through DuckDB's native ``.pl()`` result conversion, which maps
SQL types straight to polars dtypes: DATE columns become ``pl.Date`` and
TIMESTAMP columns become ``pl.Datetime``, preserving the date-vs-timestamp
distinction that the reconciliation in ``cast_columns`` depends on.
"""

from __future__ import annotations

import polars as pl


def result_dfs(pgs: dict, con) -> list[pl.DataFrame]:
    """Return one DataFrame per pgs layer, in layer order."""
    return [_query(con, layer["source_sql_query"]) for layer in pgs["layers"]]


def _query(con, sql: str) -> pl.DataFrame:
    return con.execute(sql).pl()
