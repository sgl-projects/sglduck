"""Tests for the pgs helper functions in ``utils``."""

from polars.testing import assert_series_equal
import pytest

from sglduck.cta import SglCtaAvg, SglCtaBin, SglCtaCount, SglCtaIdentity
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.utils import (
    all_aesthetics,
    col_expr_has_cta,
    column_from_aes,
    filter_agg_exprs,
    filter_col_exprs_by_cta,
)


@pytest.mark.parametrize(
    ("col_expr_cta", "cta_name", "expected_result"),
    [
        pytest.param(SglCtaIdentity(), "identity", True, id="id expr has id"),
        pytest.param(SglCtaBin(), "identity", False, id="bin expr does not have id"),
        pytest.param(SglCtaCount(), "identity", False, id="count expr does not id"),
        pytest.param(SglCtaAvg(), "identity", False, id="avg expr does not have id"),
        pytest.param(SglCtaIdentity(), "bin", False, id="id expr does not have bin"),
        pytest.param(SglCtaBin(), "bin", True, id="bin expr has bin"),
        pytest.param(SglCtaCount(), "bin", False, id="count expr does not have bin"),
        pytest.param(SglCtaAvg(), "bin", False, id="avg expr does not have bin"),
        pytest.param(SglCtaIdentity(), "count", False, id="id expr does not have count"),
        pytest.param(SglCtaBin(), "count", False, id="bin expr does not have count"),
        pytest.param(SglCtaCount(), "count", True, id="count expr has count"),
        pytest.param(SglCtaAvg(), "count", False, id="avg expr does not have count"),
        pytest.param(SglCtaIdentity(), "avg", False, id="id expr does not have avg"),
        pytest.param(SglCtaBin(), "avg", False, id="bin expr does not have avg"),
        pytest.param(SglCtaCount(), "avg", False, id="count expr does not have avg"),
        pytest.param(SglCtaAvg(), "avg", True, id="avg expr has avg"),
    ],
)
def test_col_expr_has_cta(col_expr_cta, cta_name, expected_result):
    col_expr = {"column": "col_1", "cta": col_expr_cta}

    assert col_expr_has_cta(col_expr, cta_name) is expected_result


def test_col_expr_has_cta_raises_error_for_invalid_cta_name_arg():
    col_expr = {"column": "col_1", "cta": SglCtaIdentity()}

    with pytest.raises(ValueError):
        col_expr_has_cta(col_expr, "notacta")


def test_filter_col_exprs_by_cta_returns_empty_list_for_empty_list_input():
    col_exprs = []

    assert filter_col_exprs_by_cta(col_exprs, "bin") == []


def test_filter_col_exprs_by_cta_returns_empty_list_if_none_match():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaCount()}
    col_exprs = [col_expr_1, col_expr_2]

    assert filter_col_exprs_by_cta(col_exprs, "bin") == []


def test_filter_col_exprs_by_cta_returns_single_match():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaBin()}
    col_exprs = [col_expr_1, col_expr_2]

    expected_result = [col_expr_2]

    assert filter_col_exprs_by_cta(col_exprs, "bin") == expected_result


def test_filter_col_exprs_by_cta_returns_multiple_matches():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaBin()}
    col_expr_3 = {"column": "col_3", "cta": SglCtaBin()}
    col_exprs = [col_expr_1, col_expr_2, col_expr_3]

    expected_result = [col_expr_2, col_expr_3]

    assert filter_col_exprs_by_cta(col_exprs, "bin") == expected_result


def test_filter_col_exprs_by_cta_returns_matches_for_ctas_other_than_bin():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaBin()}
    col_exprs = [col_expr_1, col_expr_2]

    expected_result = [col_expr_1]

    assert filter_col_exprs_by_cta(col_exprs, "identity") == expected_result


def test_filter_col_exprs_by_cta_raises_error_for_invalid_cta_name():
    with pytest.raises(ValueError):
        filter_col_exprs_by_cta([], "notacta")


def test_filter_agg_exprs_returns_empty_list_if_no_col_exprs_have_aggregation():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaBin()}
    col_exprs = [col_expr_1, col_expr_2]

    assert filter_agg_exprs(col_exprs) == []


def test_filter_agg_exprs_returns_agg_exprs_only():
    col_expr_1 = {"column": "col_1", "cta": SglCtaIdentity()}
    col_expr_2 = {"column": "col_2", "cta": SglCtaAvg()}
    col_expr_3 = {"column": "*", "cta": SglCtaCount()}
    col_exprs = [col_expr_1, col_expr_2, col_expr_3]

    expected_result = [col_expr_2, col_expr_3]

    assert filter_agg_exprs(col_exprs) == expected_result


def test_all_aesthetics_returns_all_aesthetics_from_single_layer_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y,
            cyl as color
        from cars
        using points
    """)

    assert set(all_aesthetics(pgs)) == {"x", "y", "color"}


def test_all_aesthetics_returns_all_aesthetics_from_all_layer_mappings():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y,
            cyl as color
        from cars
        using points

        layer

        visualize
            hp as x,
            mpg as y,
            cyl as size
        from cars
        using points
    """)

    assert set(all_aesthetics(pgs)) == {"x", "y", "color", "size"}


def test_all_aesthetics_ignores_aesthetics_from_non_visualize_clauses():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points

        scale by
            log(color)
        title
            size as 'Size'
    """)

    assert set(all_aesthetics(pgs)) == {"x", "y"}


def test_column_from_aes_returns_correct_column(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    df = dfs[0]
    layer = pgs["layers"][0]

    actual_col = column_from_aes(layer, df, "x")
    expected_col = df["hp"]
    assert_series_equal(actual_col, expected_col)
