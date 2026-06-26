"""Tests for lets_plot_direction (port of test-ggplot_orientation.R)."""

import pytest

from sglduck.lets_plot_direction import lets_plot_direction, orntn_priority_ranking
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs


def _layer_and_df(con, sgl):
    pgs = sgl_to_pgs(sgl)
    return pgs["layers"][0], result_dfs(pgs, con)[0]


@pytest.mark.parametrize(
    "col_expr,expected_priority",
    [("day", 1), ("letter", 2), ("bin(number)", 3), ("number", 4)],
)
def test_orntn_priority_ranking(test_con, col_expr, expected_priority):
    layer, df = _layer_and_df(
        test_con, f"visualize {col_expr} as x from synth using bars"
    )
    assert orntn_priority_ranking(layer, df, "x") == expected_priority


@pytest.mark.parametrize(
    "geom,qual,expected_orientation",
    [
        ("line", "horizontal", "x"),
        ("line", "vertical", "y"),
        ("bar", "horizontal", "y"),
        ("bar", "vertical", "x"),
    ],
)
def test_orientation_from_direction_qualifier(
    test_con, geom, qual, expected_orientation
):
    layer, df = _layer_and_df(
        test_con, f"visualize hp as x, mpg as y from cars using {qual} {geom}"
    )
    assert lets_plot_direction(layer, df) == expected_orientation


@pytest.mark.parametrize(
    "aes,expected_orientation",
    [("x", "y"), ("y", "x"), ("theta", "y"), ("r", "x")],
)
def test_orientation_with_one_positional_aes(test_con, aes, expected_orientation):
    layer, df = _layer_and_df(
        test_con, f"visualize hp as {aes} from cars using bars"
    )
    assert lets_plot_direction(layer, df) == expected_orientation


@pytest.mark.parametrize(
    "collected_aes,uncollected_aes,expected_orientation",
    [("x", "y", "x"), ("y", "x", "y"), ("theta", "r", "x"), ("r", "theta", "y")],
)
def test_orientation_for_box_with_collection(
    test_con, collected_aes, uncollected_aes, expected_orientation
):
    layer, df = _layer_and_df(
        test_con,
        f"visualize cyl as {collected_aes}, mpg as {uncollected_aes} "
        f"from cars collect by cyl using boxes",
    )
    assert lets_plot_direction(layer, df) == expected_orientation


@pytest.mark.parametrize(
    "aes_1,aes_2,expr_1,expr_2,expected_orientation",
    [
        # ties go to x
        ("x", "y", "day", "number", "x"),
        ("y", "x", "day", "number", "y"),
        ("x", "y", "day", "day_and_time", "x"),
        ("theta", "r", "day", "number", "x"),
        ("r", "theta", "day", "number", "y"),
        ("theta", "r", "day", "day_and_time", "x"),
    ],
)
def test_orientation_from_priority_ranking(
    test_con, aes_1, aes_2, expr_1, expr_2, expected_orientation
):
    layer, df = _layer_and_df(
        test_con,
        f"visualize {expr_1} as {aes_1}, {expr_2} as {aes_2} "
        f"from synth using boxes",
    )
    assert lets_plot_direction(layer, df) == expected_orientation
