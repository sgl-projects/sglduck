"""Shared pytest fixtures and data loading.

Mirrors rsgl's ``tests/testthat/setup.R`` + ``R/create_con_and_load_data.R``:
builds a DuckDB connection loaded with the ``cars`` (mtcars), ``economics``,
``synth``, and ``diamonds`` tables used across the test suite.
"""

from __future__ import annotations

import duckdb
import pandas as pd
import pytest
from plotnine.data import diamonds, economics, mtcars


def create_con_and_load_data():
    """Create a DuckDB connection and load the test tables."""
    con = duckdb.connect()

    _write_table(con, "cars", mtcars)
    _write_table(con, "economics", economics)

    # synth carries a DATE column (``day``) and a TIMESTAMP column
    # (``day_and_time``) sharing the same instants, for the date-vs-timestamp
    # reconciliation tests; both step by 10 years from 1950-01-01.
    instants = pd.date_range("1950-01-01", periods=6, freq="10YS")
    synth = pd.DataFrame(
        {
            "letter": list("abc") * 2,
            "number": range(1, 7),
            "day": instants,
            "day_and_time": instants,
            "boolean": [True] * 3 + [False] * 3,
        }
    )
    con.register("synth_df", synth)
    con.execute(
        """
        create table synth as
        select
            letter,
            number,
            cast(day as date) as day,
            cast(day_and_time as timestamp) as day_and_time,
            boolean
        from synth_df
        """
    )
    con.unregister("synth_df")

    _write_table(con, "diamonds", diamonds)
    return con


def _write_table(con, name: str, df: pd.DataFrame) -> None:
    con.register(f"{name}_df", df)
    con.execute(f"create table {name} as select * from {name}_df")
    con.unregister(f"{name}_df")


@pytest.fixture(scope="session")
def test_con():
    con = create_con_and_load_data()
    yield con
    con.close()
