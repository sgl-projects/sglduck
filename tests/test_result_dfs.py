"""Tests for ``result_dfs`` (port of rsgl's test-result_dfs.R)."""

import pandas as pd
import pytest

from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs


def test_returns_correct_dataframe_for_table_name_source(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)

    actual_dfs = result_dfs(pgs, test_con)

    expected_df = test_con.execute("select * from cars").df()
    pd.testing.assert_frame_equal(actual_dfs[0], expected_df)


def test_returns_correct_dataframe_for_subquery_source(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from (
            select *
            from cars
            where cyl = 4
        )
        using points
    """)

    actual_dfs = result_dfs(pgs, test_con)

    expected_df = test_con.execute("""
        select *
        from cars
        where cyl = 4
    """).df()
    pd.testing.assert_frame_equal(actual_dfs[0], expected_df)


def test_raises_error_if_table_doesnt_exist(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cty as x,
            hwy as y
        from not_cars
        using points
    """)

    with pytest.raises(Exception, match="Table with name not_cars does not exist"):
        result_dfs(pgs, test_con)


def test_raises_error_for_invalid_subquery(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cty as x,
            hwy as y
        from (select something)
        using points
    """)

    expected_msg = (
        'Referenced column "something" was not found '
        "because the FROM clause is missing"
    )
    with pytest.raises(Exception, match=expected_msg):
        result_dfs(pgs, test_con)


def test_returns_single_df_for_single_layer(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)

    actual_dfs = result_dfs(pgs, test_con)

    assert len(actual_dfs) == 1


def test_returns_multiple_dfs_for_multiple_layers(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points

        layer

        visualize
            hp as x,
            mpg as y
        from (
            select *
            from cars
            where cyl = 4
        )
        using points
    """)

    actual_dfs = result_dfs(pgs, test_con)

    expected_df_1 = test_con.execute("select * from cars").df()
    expected_df_2 = test_con.execute("""
        select *
        from cars
        where cyl = 4
    """).df()
    assert len(actual_dfs) == 2
    pd.testing.assert_frame_equal(actual_dfs[0], expected_df_1)
    pd.testing.assert_frame_equal(actual_dfs[1], expected_df_2)
