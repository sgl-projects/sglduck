"""Tests for perform_ctas (port of test-perform_ctas.R)."""

import pandas as pd

from pysgl.perform_as_for_layer import perform_as_for_layer
from pysgl.perform_cts_for_layer import perform_cts_for_layer
from pysgl.perform_ctas import perform_ctas
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs


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


def _expected_for_layer(layer, df, scales):
    transformed = perform_cts_for_layer(layer, df, scales)
    return perform_as_for_layer(layer, transformed, scales)


def test_doesnt_modify_dataframe_if_no_ctas(test_con):
    pgs = sgl_to_pgs("visualize hp as x, mpg as y from cars using points")
    input_dfs = result_dfs(pgs, test_con)

    actual = perform_ctas(pgs, input_dfs)

    assert len(actual) == len(input_dfs)
    _assert_equal(actual[0], input_dfs[0])


def test_performs_ctas_for_single_layer(test_con):
    pgs = sgl_to_pgs(
        """
        visualize bin(mpg) as x, count(*) as y
        from cars group by bin(mpg) using bars
        """
    )
    input_dfs = result_dfs(pgs, test_con)
    scales = pgs.get("scales")

    actual = perform_ctas(pgs, input_dfs)

    expected = [_expected_for_layer(pgs["layers"][0], input_dfs[0], scales)]
    assert len(actual) == len(expected)
    _assert_equal(actual[0], expected[0])


def test_performs_ctas_for_transformed_and_leaves_untransformed(test_con):
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y
        from cars using points

        layer

        visualize bin(mpg) as x, count(*) as y
        from cars group by bin(mpg) using bars
        """
    )
    input_dfs = result_dfs(pgs, test_con)
    scales = pgs.get("scales")

    actual = perform_ctas(pgs, input_dfs)

    expected = [
        input_dfs[0],
        _expected_for_layer(pgs["layers"][1], input_dfs[1], scales),
    ]
    assert len(actual) == len(expected)
    _assert_equal(actual[0], expected[0])
    _assert_equal(actual[1], expected[1])


def test_performs_ctas_for_multiple_transformed_layers(test_con):
    pgs = sgl_to_pgs(
        """
        visualize cyl as x, count(*) as y
        from cars group by cyl using points

        layer

        visualize bin(mpg) as x, count(*) as y
        from cars group by bin(mpg) using bars
        """
    )
    input_dfs = result_dfs(pgs, test_con)
    scales = pgs.get("scales")

    actual = perform_ctas(pgs, input_dfs)

    expected = [
        _expected_for_layer(pgs["layers"][0], input_dfs[0], scales),
        _expected_for_layer(pgs["layers"][1], input_dfs[1], scales),
    ]
    assert len(actual) == len(expected)
    _assert_equal(actual[0], expected[0])
    _assert_equal(actual[1], expected[1])
