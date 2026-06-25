"""Tests for perform_as_for_layer (port of test-perform_as_for_layer.R)."""

import numpy as np
import pandas as pd

from sglduck.cta import Aggregation, SglCtaBin
from sglduck.perform_as_for_layer import (
    add_scaled_cols,
    perform_as_for_layer,
    summarize_args,
)
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.scale import SglScaleLinear


def _normalize(df):
    df = df.reset_index(drop=True)
    df = df.reindex(sorted(df.columns), axis=1)
    if len(df.columns):
        df = df.sort_values(list(df.columns), na_position="last", kind="stable")
    return df.reset_index(drop=True)


def _assert_equal(actual, expected):
    pd.testing.assert_frame_equal(
        _normalize(actual), _normalize(expected), check_dtype=False
    )


def _layer_and_df(sgl_stmt, test_con):
    pgs = sgl_to_pgs(sgl_stmt)
    df = result_dfs(pgs, test_con)[0]
    return pgs["layers"][0], df, pgs.get("scales")


def _binned(column, df, scale, num_bins=30):
    return SglCtaBin().add_transformed_column(column, df, scale, num_bins=num_bins)


def _grouped_summary(df, group_cols, aggs, backscale=()):
    grouped = df.groupby(group_cols, dropna=False, sort=False)
    cols = {}
    for name, (func, col) in aggs.items():
        cols[name] = grouped.size() if func == "size" else grouped[col].agg(func)
    out = pd.concat(cols, axis=1).reset_index()
    for name in backscale:
        out[name] = np.power(10.0, out[name])
    return out


class TestAddScaledCols:
    def test_no_scale_returns_original(self, test_con):
        layer, df, scales = _layer_and_df(
            "visualize hp as x, mpg as y from cars using points", test_con
        )
        _assert_equal(add_scaled_cols(layer, scales, df), df)

    def test_no_scaled_agg_needs_scaling_returns_original(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, count(*) as y
            from cars group by bin(mpg) using bars scale by log(y)
            """,
            test_con,
        )
        _assert_equal(add_scaled_cols(layer, scales, df), df)

    def test_one_scaled_agg(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y
            from cars group by bin(mpg) using bars scale by log(y)
            """,
            test_con,
        )
        expected = df.assign(**{"sglduck.log.hp": np.log10(df["hp"])})
        _assert_equal(add_scaled_cols(layer, scales, df), expected)

    def test_multiple_distinct_scaled_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, avg(cyl) as color
            from cars group by bin(mpg) using bars scale by log(y), log(color)
            """,
            test_con,
        )
        expected = df.assign(
            **{"sglduck.log.hp": np.log10(df["hp"]), "sglduck.log.cyl": np.log10(df["cyl"])}
        )
        _assert_equal(add_scaled_cols(layer, scales, df), expected)

    def test_same_mapping_not_duplicated(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, avg(hp) as color
            from cars group by bin(mpg) using bars scale by log(y), log(color)
            """,
            test_con,
        )
        expected = df.assign(**{"sglduck.log.hp": np.log10(df["hp"])})
        _assert_equal(add_scaled_cols(layer, scales, df), expected)

    def test_multiple_scale_types_no_duplication(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, avg(hp) as color, avg(hp) as size
            from cars group by bin(mpg) using points
            scale by log(y), log(color), ln(size)
            """,
            test_con,
        )
        expected = df.assign(
            **{"sglduck.log.hp": np.log10(df["hp"]), "sglduck.ln.hp": np.log(df["hp"])}
        )
        _assert_equal(add_scaled_cols(layer, scales, df), expected)


class TestSummarizeArgs:
    def test_count_without_scale(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, count(*) as y
            from cars group by bin(mpg) using bars scale by log(y)
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.count": Aggregation("size", None)
        }

    def test_avg_with_default_scale(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y
            from cars group by bin(mpg) using bars
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.linear.avg.hp": Aggregation("mean", "hp")
        }

    def test_avg_with_non_default_scale(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y
            from cars group by bin(mpg) using bars scale by log(y)
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.log.avg.hp": Aggregation("mean", "sglduck.log.hp")
        }

    def test_multiple_aggs(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, avg(cyl) as color, count(*) as size
            from cars group by bin(mpg) using points scale by log(y)
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.log.avg.hp": Aggregation("mean", "sglduck.log.hp"),
            "sglduck.linear.avg.cyl": Aggregation("mean", "cyl"),
            "sglduck.count": Aggregation("size", None),
        }

    def test_aggs_in_collect_by_only(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize vs as x, am as y
            from cars group by vs, am
            collect by count(*), avg(hp), avg(mpg) using points
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.linear.avg.hp": Aggregation("mean", "hp"),
            "sglduck.linear.avg.mpg": Aggregation("mean", "mpg"),
            "sglduck.count": Aggregation("size", None),
        }

    def test_aggs_in_mapping_and_collect_no_duplication(self, test_con):
        layer, _, scales = _layer_and_df(
            """
            visualize vs as x, am as y, avg(hp) as color
            from cars group by vs, am
            collect by count(*), avg(hp), avg(mpg) using lines scale by log(color)
            """,
            test_con,
        )
        assert summarize_args(layer, scales) == {
            "sglduck.log.avg.hp": Aggregation("mean", "sglduck.log.hp"),
            "sglduck.linear.avg.mpg": Aggregation("mean", "mpg"),
            "sglduck.count": Aggregation("size", None),
        }


class TestPerformAsForLayer:
    def test_no_aggregations_returns_input(self, test_con):
        layer, df, scales = _layer_and_df(
            "visualize hp as x, mpg as y from cars using points", test_con
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), df)

    def test_no_grouping_all_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            "visualize count(*) as x from cars collect by avg(mpg) using lines",
            test_con,
        )
        expected = pd.DataFrame(
            [{"sglduck.count": len(df), "sglduck.linear.avg.mpg": df["mpg"].mean()}]
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)

    def test_untransformed_col_and_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize vs_cat as x, avg(mpg) as y, count(*) as color
            from (select *, cast(vs as varchar) as vs_cat from cars)
            group by vs_cat using bars
            """,
            test_con,
        )
        expected = _grouped_summary(
            df,
            ["vs_cat"],
            {
                "sglduck.linear.avg.mpg": ("mean", "mpg"),
                "sglduck.count": ("size", None),
            },
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)

    def test_binned_col_and_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, count(*) as color
            from cars group by bin(mpg) using bars
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLinear())
        expected = _grouped_summary(
            transformed,
            ["sglduck.linear.bin.30.mpg"],
            {
                "sglduck.linear.avg.hp": ("mean", "hp"),
                "sglduck.count": ("size", None),
            },
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_binned_col_with_arg_and_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg, 5) as x, avg(hp) as y, count(*) as color
            from cars group by bin(mpg, 5) using bars
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLinear(), num_bins=5)
        expected = _grouped_summary(
            transformed,
            ["sglduck.linear.bin.5.mpg"],
            {
                "sglduck.linear.avg.hp": ("mean", "hp"),
                "sglduck.count": ("size", None),
            },
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_non_linear_scaled_binned_col(self, test_con):
        from sglduck.scale import SglScaleLog

        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, avg(hp) as y, count(*) as color
            from cars group by bin(mpg) using bars scale by log(x)
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLog())
        expected = _grouped_summary(
            transformed,
            ["sglduck.log.bin.30.mpg"],
            {
                "sglduck.linear.avg.hp": ("mean", "hp"),
                "sglduck.count": ("size", None),
            },
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_binned_cols_for_multiple_scales(self, test_con):
        from sglduck.scale import SglScaleLn, SglScaleLog

        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, bin(mpg) as y, count(*) as color, bin(mpg) as size
            from cars group by bin(mpg) using bars scale by log(y), ln(size)
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLog())
        transformed = _binned("mpg", transformed, SglScaleLn())
        transformed = _binned("mpg", transformed, SglScaleLinear())
        expected = _grouped_summary(
            transformed,
            [
                "sglduck.log.bin.30.mpg",
                "sglduck.ln.bin.30.mpg",
                "sglduck.linear.bin.30.mpg",
            ],
            {"sglduck.count": ("size", None)},
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_binned_and_unbinned_col_and_aggs(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, count(*) as y, vs_cat as color, avg(hp) as size
            from (select *, cast(vs as varchar) as vs_cat from cars)
            group by bin(mpg), vs_cat using points
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLinear())
        expected = _grouped_summary(
            transformed,
            ["sglduck.linear.bin.30.mpg", "vs_cat"],
            {
                "sglduck.count": ("size", None),
                "sglduck.linear.avg.hp": ("mean", "hp"),
            },
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_additional_grouping_not_in_aes_mapping(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize bin(mpg) as x, count(*) as y
            from (select *, cast(vs as varchar) as vs_cat from cars)
            group by bin(mpg), vs_cat using bars
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLinear())
        expected = _grouped_summary(
            transformed,
            ["sglduck.linear.bin.30.mpg", "vs_cat"],
            {"sglduck.count": ("size", None)},
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_additional_binned_grouping_not_in_aes_mapping(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize vs_cat as x, count(*) as y
            from (select *, cast(vs as varchar) as vs_cat from cars)
            group by vs_cat, bin(mpg) using bars
            """,
            test_con,
        )
        transformed = _binned("mpg", df, SglScaleLinear())
        expected = _grouped_summary(
            transformed,
            ["vs_cat", "sglduck.linear.bin.30.mpg"],
            {"sglduck.count": ("size", None)},
        )
        _assert_equal(perform_as_for_layer(layer, transformed, scales), expected)

    def test_aggs_from_collection(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize hp as x, mpg as y
            from cars group by hp, mpg
            collect by count(*), avg(cyl) using lines
            """,
            test_con,
        )
        expected = _grouped_summary(
            df,
            ["hp", "mpg"],
            {
                "sglduck.count": ("size", None),
                "sglduck.linear.avg.cyl": ("mean", "cyl"),
            },
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)

    def test_aggs_from_mapping_and_collection_no_duplication(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize hp as x, mpg as y, avg(hp) as color
            from cars group by hp, mpg
            collect by count(*), avg(hp) using lines
            """,
            test_con,
        )
        expected = _grouped_summary(
            df,
            ["hp", "mpg"],
            {
                "sglduck.count": ("size", None),
                "sglduck.linear.avg.hp": ("mean", "hp"),
            },
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)

    def test_takes_scales_into_account_for_agg(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize hp as x, mpg as y, avg(cyl) as color
            from cars group by hp, mpg
            collect by avg(cyl), avg(vs) using lines scale by log(color)
            """,
            test_con,
        )
        scaled = df.assign(**{"sglduck.log.cyl": np.log10(df["cyl"])})
        expected = _grouped_summary(
            scaled,
            ["hp", "mpg"],
            {
                "sglduck.linear.avg.vs": ("mean", "vs"),
                "sglduck.log.avg.cyl": ("mean", "sglduck.log.cyl"),
            },
            backscale=["sglduck.log.avg.cyl"],
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)

    def test_only_backscales_aggs_once(self, test_con):
        layer, df, scales = _layer_and_df(
            """
            visualize hp as x, mpg as y, avg(cyl) as color, avg(cyl) as size
            from cars group by hp, mpg using points scale by log(color), log(size)
            """,
            test_con,
        )
        scaled = df.assign(**{"sglduck.log.cyl": np.log10(df["cyl"])})
        expected = _grouped_summary(
            scaled,
            ["hp", "mpg"],
            {"sglduck.log.avg.cyl": ("mean", "sglduck.log.cyl")},
            backscale=["sglduck.log.avg.cyl"],
        )
        _assert_equal(perform_as_for_layer(layer, df, scales), expected)
