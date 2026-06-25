"""Tests for column_exists and valid_column_refs."""

import re

import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.validate import valid_column_refs
from sglduck.validate.valid_column_refs import column_exists


def test_column_exists_returns_true_for_wildcard_regardless_of_cta(test_con):
    pgs = sgl_to_pgs("""
        visualize
            * as x,
            bin(*) as y,
            count(*) as color
        from cars
        using points
    """)
    df = result_dfs(pgs, test_con)[0]
    col_exprs = list(pgs["layers"][0]["aes_mappings"].values())

    assert column_exists(col_exprs, df) == {"*": True}


def test_column_exists_returns_true_for_existing_columns_regardless_of_cta(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            bin(mpg) as y,
            count(cyl) as color
        from cars
        using points
    """)
    df = result_dfs(pgs, test_con)[0]
    col_exprs = list(pgs["layers"][0]["aes_mappings"].values())

    assert column_exists(col_exprs, df) == {"cyl": True, "mpg": True, "hp": True}


def test_column_exists_returns_false_for_missing_columns_regardless_of_cta(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            not_a_col_1 as x,
            bin(not_a_col_2) as y,
            count(not_a_col_3) as color
        from cars
        using points
    """)
    df = result_dfs(pgs, test_con)[0]
    col_exprs = list(pgs["layers"][0]["aes_mappings"].values())

    assert column_exists(col_exprs, df) == {
        "not_a_col_1": False,
        "not_a_col_2": False,
        "not_a_col_3": False,
    }


def test_column_exists_handles_mixture_of_existing_and_missing_columns(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            not_a_col as y,
            * as color
        from cars
        using points
    """)
    df = result_dfs(pgs, test_con)[0]
    col_exprs = list(pgs["layers"][0]["aes_mappings"].values())

    assert column_exists(col_exprs, df) == {
        "*": True,
        "not_a_col": False,
        "hp": True,
    }


def test_column_exists_doesnt_duplicate_results(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            bin(hp) as y,
            not_a_col_1 as theta,
            count(not_a_col_1) as r,
            bin(*) as color,
            count(*) as size
        from cars
        using points
    """)
    df = result_dfs(pgs, test_con)[0]
    col_exprs = list(pgs["layers"][0]["aes_mappings"].values())

    assert column_exists(col_exprs, df) == {
        "*": True,
        "not_a_col_1": False,
        "hp": True,
    }


def test_valid_column_refs_allows_valid_refs_in_all_clauses(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cut as x,
            count(*) as y,
            clarity as color
        from diamonds
        group by
            cut,
            clarity
        collect by
            clarity
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, test_con)[0]

    valid_column_refs(layer, df)


def test_valid_column_refs_raises_error_for_invalid_ref_in_visualize_clause(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            cut as x,
            count(not_a_col) as y,
            clarity as color
        from diamonds
        group by
            cut,
            clarity
        collect by
            clarity
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, test_con)[0]

    with pytest.raises(
        SglError,
        match=re.escape("Error: referenced column 'not_a_col' not found"),
    ):
        valid_column_refs(layer, df)


def test_valid_column_refs_raises_error_for_invalid_ref_in_group_by_clause(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            cut as x,
            count(*) as y,
            clarity as color
        from diamonds
        group by
            cut,
            not_a_col
        collect by
            clarity
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, test_con)[0]

    with pytest.raises(
        SglError,
        match=re.escape("Error: referenced column 'not_a_col' not found"),
    ):
        valid_column_refs(layer, df)


def test_valid_column_refs_raises_error_for_invalid_ref_in_collect_by_clause(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            cut as x,
            count(*) as y,
            clarity as color
        from diamonds
        group by
            cut,
            clarity
        collect by
            not_a_col
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, test_con)[0]

    with pytest.raises(
        SglError,
        match=re.escape("Error: referenced column 'not_a_col' not found"),
    ):
        valid_column_refs(layer, df)
