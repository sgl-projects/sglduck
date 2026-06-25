"""Tests for db_get_plot (port of test-dbGetPlot.R)."""

from sglduck import SglPlot, db_get_plot
from sglduck.match_col_casing import match_col_casing
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs

TEST_SGL_STMT = """
  visualize
    HP as x,
    mpg as y
  from cars
  using points

  layer

  visualize
    carat as x,
    price as y
  from diamonds
  using points
"""


def test_returns_sgl_plot(test_con):
    assert isinstance(db_get_plot(test_con, TEST_SGL_STMT), SglPlot)


def test_holds_matched_casing_pgs(test_con):
    plot = db_get_plot(test_con, TEST_SGL_STMT)

    pgs = sgl_to_pgs(TEST_SGL_STMT)
    dfs = result_dfs(pgs, test_con)
    expected_pgs = match_col_casing(pgs, dfs)

    assert plot.pgs == expected_pgs


def test_holds_result_dfs(test_con):
    plot = db_get_plot(test_con, TEST_SGL_STMT)

    pgs = sgl_to_pgs(TEST_SGL_STMT)
    expected_dfs = result_dfs(pgs, test_con)

    assert len(plot.result_dfs) == len(expected_dfs)
    assert all(
        actual.equals(expected)
        for actual, expected in zip(plot.result_dfs, expected_dfs)
    )
