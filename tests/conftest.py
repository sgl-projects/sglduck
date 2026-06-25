"""Shared pytest fixtures and data loading.

Builds a DuckDB connection loaded with the ``cars`` (mtcars), ``economics``,
``synth``, and ``diamonds`` tables used across the test suite. The mtcars,
economics, and diamonds datasets are vendored as CSV files under ``tests/data``.
"""

from __future__ import annotations

import datetime

from pathlib import Path

import duckdb
import polars as pl
import pytest

_DATA_DIR = Path(__file__).parent / "data"


def create_con_and_load_data():
    """Create a DuckDB connection and load the test tables."""
    con = duckdb.connect()

    _write_table(con, "cars", pl.read_csv(_DATA_DIR / "mtcars.csv"))
    _write_table(
        con,
        "economics",
        pl.read_csv(_DATA_DIR / "economics.csv", try_parse_dates=True),
    )

    # synth carries a DATE column (``day``) and a TIMESTAMP column
    # (``day_and_time``) sharing the same instants, for the date-vs-timestamp
    # reconciliation tests; both step by 10 years from 1950-01-01.
    instants = [datetime.datetime(1950 + 10 * i, 1, 1) for i in range(6)]
    synth = pl.DataFrame(
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

    _write_table(con, "diamonds", pl.read_csv(_DATA_DIR / "diamonds.csv"))
    return con


def _write_table(con, name: str, df: pl.DataFrame) -> None:
    con.register(f"{name}_df", df)
    con.execute(f"create table {name} as select * from {name}_df")
    con.unregister(f"{name}_df")


@pytest.fixture(scope="session")
def test_con():
    con = create_con_and_load_data()
    yield con
    con.close()


@pytest.fixture
def synth_with_blob_col(test_con):
    """Temporarily add a BLOB column (unknown SGL classification) to synth.

    Cleanup is an explicit add/drop of the column rather than wrapping the
    test in a transaction, keeping the fixture independent of DuckDB's
    transaction state.
    """
    test_con.execute("alter table synth add column blob_col BLOB")
    yield test_con
    test_con.execute("alter table synth drop column blob_col")
