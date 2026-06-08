"""Run each layer's source SQL query into a pandas DataFrame.

Analog of rsgl's ``R/result_dfs.R``: maps each pgs layer to the DataFrame
produced by executing its ``source_sql_query`` against the supplied database
connection. ``con`` is anything ``pandas.read_sql_query`` accepts — a SQLAlchemy
engine/connection or any DB-API 2.0 (PEP 249) connection (e.g. DuckDB,
sqlite3) — mirroring how rsgl's ``DBI::dbGetQuery`` runs against any DBI
connection.
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
        # SQLAlchemy + sqlite3), but the DB-API path works fine — suppress the
        # cosmetic nag so it doesn't surface to users on every plot.
        warnings.filterwarnings(
            "ignore",
            message="pandas only supports SQLAlchemy connectable",
            category=UserWarning,
        )
        return pd.read_sql_query(sql, con)
