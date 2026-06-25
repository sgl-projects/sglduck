"""Tests for perform_cts_for_layer (port of test-perform_cts_for_layer.R)."""

import pandas as pd

from sglduck.cta import SglCtaBin
from sglduck.perform_cts_for_layer import perform_cts_for_layer
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.scale import SglScaleLinear, SglScaleLog


def _cts(sgl_stmt, test_con):
    pgs = sgl_to_pgs(sgl_stmt)
    df = result_dfs(pgs, test_con)[0]
    return perform_cts_for_layer(pgs["layers"][0], df, pgs.get("scales")), df


def _binned(column, df, scale, num_bins=30):
    return SglCtaBin().add_transformed_column(column, df, scale, num_bins=num_bins)


def _assert_equal(actual, expected):
    pd.testing.assert_frame_equal(actual, expected, check_like=True)


class TestNoTransformations:
    def test_returns_original_dataframe(self, test_con):
        result, input_df = _cts(
            """
            visualize cut as x, count(*) as y
            from diamonds
            group by cut, color
            collect by color
            using lines
            """,
            test_con,
        )
        _assert_equal(result, input_df)


class TestVisualizeClauseOnly:
    def test_single_default_scaling(self, test_con):
        result, input_df = _cts(
            "visualize bin(mpg) as x from cars using points", test_con
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear()))

    def test_single_non_default_scaling(self, test_con):
        result, input_df = _cts(
            "visualize bin(mpg) as x from cars using points scale by log(x)",
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLog()))

    def test_single_with_arg(self, test_con):
        result, input_df = _cts(
            "visualize bin(mpg, 5) as x from cars using points", test_con
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear(), num_bins=5))

    def test_same_col_same_scale_no_duplicate(self, test_con):
        result, input_df = _cts(
            "visualize bin(mpg) as x, bin(mpg) as y from cars using points",
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear()))

    def test_same_col_different_scales(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, bin(mpg) as y
            from cars using points scale by log(y)
            """,
            test_con,
        )
        expected = _binned("mpg", input_df, SglScaleLog())
        expected = _binned("mpg", expected, SglScaleLinear())
        _assert_equal(result, expected)

    def test_different_col_exprs(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, bin(mpg, 5) as y, bin(hp) as color
            from cars using points
            """,
            test_con,
        )
        expected = _binned("hp", input_df, SglScaleLinear())
        expected = _binned("mpg", expected, SglScaleLinear(), num_bins=5)
        expected = _binned("mpg", expected, SglScaleLinear())
        _assert_equal(result, expected)

    def test_ignores_untransformed_columns(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, bin(hp) as y, cyl as color
            from cars using points scale by log(color)
            """,
            test_con,
        )
        expected = _binned("hp", input_df, SglScaleLinear())
        expected = _binned("mpg", expected, SglScaleLinear())
        _assert_equal(result, expected)


class TestGroupByClauseOnly:
    def test_single_default_scaling(self, test_con):
        result, input_df = _cts(
            "visualize count(*) as x from cars group by bin(mpg) using points",
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear()))

    def test_single_with_arg(self, test_con):
        result, input_df = _cts(
            "visualize count(*) as x from cars group by bin(mpg, 5) using points",
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear(), num_bins=5))

    def test_multiple_default_scaling(self, test_con):
        result, input_df = _cts(
            """
            visualize count(*) as x
            from cars group by bin(mpg), bin(hp) using points
            """,
            test_con,
        )
        expected = _binned("hp", input_df, SglScaleLinear())
        expected = _binned("mpg", expected, SglScaleLinear())
        _assert_equal(result, expected)

    def test_ignores_untransformed_expression(self, test_con):
        result, input_df = _cts(
            """
            visualize cyl as x, count(*) as y
            from cars group by cyl, bin(mpg) using points
            """,
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLinear()))


class TestCollectByClauseOnly:
    def test_single_default_scaling(self, test_con):
        result, input_df = _cts(
            """
            visualize hp as x, mpg as y
            from cars collect by bin(wt) using lines
            """,
            test_con,
        )
        _assert_equal(result, _binned("wt", input_df, SglScaleLinear()))

    def test_single_with_arg(self, test_con):
        result, input_df = _cts(
            """
            visualize hp as x, mpg as y
            from cars collect by bin(wt, 5) using lines
            """,
            test_con,
        )
        _assert_equal(result, _binned("wt", input_df, SglScaleLinear(), num_bins=5))

    def test_multiple_default_scaling(self, test_con):
        result, input_df = _cts(
            """
            visualize hp as x, mpg as y
            from cars collect by bin(wt), bin(disp) using lines
            """,
            test_con,
        )
        expected = _binned("disp", input_df, SglScaleLinear())
        expected = _binned("wt", expected, SglScaleLinear())
        _assert_equal(result, expected)

    def test_ignores_untransformed_expression(self, test_con):
        result, input_df = _cts(
            """
            visualize hp as x, mpg as y
            from cars collect by bin(wt), bin(disp), cyl using lines
            """,
            test_con,
        )
        expected = _binned("disp", input_df, SglScaleLinear())
        expected = _binned("wt", expected, SglScaleLinear())
        _assert_equal(result, expected)


class TestVisualizeAndGroupBy:
    def test_same_trans_exprs_no_extra_cols(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, count(*) as y, bin(hp, 5) as color
            from cars group by bin(mpg), bin(hp, 5) using points scale by log(color)
            """,
            test_con,
        )
        expected = _binned("hp", input_df, SglScaleLog(), num_bins=5)
        expected = _binned("mpg", expected, SglScaleLinear())
        _assert_equal(result, expected)

    def test_group_by_has_additional_trans_exprs(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, count(*) as y
            from cars group by bin(mpg), bin(mpg, 5), bin(hp) using points
            """,
            test_con,
        )
        expected = _binned("mpg", input_df, SglScaleLinear())
        expected = _binned("hp", expected, SglScaleLinear())
        expected = _binned("mpg", expected, SglScaleLinear(), num_bins=5)
        _assert_equal(result, expected)


class TestVisualizeAndCollectBy:
    def test_same_trans_exprs_no_extra_cols(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, hp as y
            from cars collect by bin(mpg) using boxes scale by log(x)
            """,
            test_con,
        )
        _assert_equal(result, _binned("mpg", input_df, SglScaleLog()))

    def test_different_trans_exprs(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(mpg) as x, hp as y, bin(disp) as color
            from cars collect by bin(disp), bin(mpg, 5), bin(wt)
            using points scale by log(color)
            """,
            test_con,
        )
        expected = _binned("disp", input_df, SglScaleLog())
        expected = _binned("mpg", expected, SglScaleLinear())
        expected = _binned("wt", expected, SglScaleLinear())
        expected = _binned("mpg", expected, SglScaleLinear(), num_bins=5)
        _assert_equal(result, expected)


class TestGroupByAndCollectBy:
    def test_same_trans_exprs_no_duplication(self, test_con):
        result, input_df = _cts(
            """
            visualize cut as x, count(*) as y
            from diamonds
            group by bin(carat, 5), bin(price)
            collect by bin(carat, 5), bin(price)
            using lines
            """,
            test_con,
        )
        expected = _binned("price", input_df, SglScaleLinear())
        expected = _binned("carat", expected, SglScaleLinear(), num_bins=5)
        _assert_equal(result, expected)

    def test_collect_subset_of_group_by(self, test_con):
        result, input_df = _cts(
            """
            visualize cut as x, count(*) as y
            from diamonds
            group by bin(carat), bin(price)
            collect by bin(price)
            using lines
            """,
            test_con,
        )
        expected = _binned("price", input_df, SglScaleLinear())
        expected = _binned("carat", expected, SglScaleLinear())
        _assert_equal(result, expected)


class TestAllThreeClauses:
    def test_adds_all_without_duplication(self, test_con):
        result, input_df = _cts(
            """
            visualize bin(carat) as x, count(*) as y
            from diamonds
            group by bin(carat), bin(price)
            collect by bin(price)
            using lines scale by log(x)
            """,
            test_con,
        )
        expected = _binned("carat", input_df, SglScaleLog())
        expected = _binned("price", expected, SglScaleLinear())
        _assert_equal(result, expected)
