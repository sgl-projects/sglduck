"""Tests for valid_column_class and valid_column_classes."""

import re

import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.validate import valid_column_class, valid_column_classes

UNKNOWN_CLASS_MSG = (
    "Error: unknown SGL type classification"
    " (numerical, categorical, or temporal)"
    " for column 'blob_col'."
)


def synth_df(con):
    # `from synth` expands to `select * from synth`, so this fetches the
    # whole table through the same query path as the pipeline
    pgs = sgl_to_pgs("""
        visualize
            number as x
        from synth
        using points
    """)
    return result_dfs(pgs, con)[0]


@pytest.mark.parametrize(
    "column",
    [
        pytest.param("*", id="wildcard"),
        pytest.param("number", id="numerical"),
        pytest.param("letter", id="categorical"),
        pytest.param("day", id="temporal"),
    ],
)
def test_valid_column_class_allows_known_classes(test_con, column):
    test_df = synth_df(test_con)

    valid_column_class(column, test_df)


def test_valid_column_class_raises_error_for_unknown_class(synth_with_blob_col):
    test_df_w_blob = synth_df(synth_with_blob_col)

    with pytest.raises(SglError, match=re.escape(UNKNOWN_CLASS_MSG)):
        valid_column_class("blob_col", test_df_w_blob)


def test_doesnt_raise_error_if_all_classes_are_valid_in_all_clauses(test_con):
    pgs = sgl_to_pgs("""
        visualize
            letter as x,
            count(*) as y
        from synth
        group by
            letter
        collect by
            boolean
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, test_con)[0]

    valid_column_classes(layer, df)


def test_raises_error_for_invalid_class_in_visualize_clause(synth_with_blob_col):
    pgs = sgl_to_pgs("""
        visualize
            blob_col as x,
            number as y
        from synth
        using points
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, synth_with_blob_col)[0]

    with pytest.raises(SglError, match=re.escape(UNKNOWN_CLASS_MSG)):
        valid_column_classes(layer, df)


def test_raises_error_for_invalid_class_in_group_by_clause(synth_with_blob_col):
    pgs = sgl_to_pgs("""
        visualize
            count(*) as x
        from synth
        group by
            blob_col
        using points
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, synth_with_blob_col)[0]

    with pytest.raises(SglError, match=re.escape(UNKNOWN_CLASS_MSG)):
        valid_column_classes(layer, df)


def test_raises_error_for_invalid_class_in_collect_by_clause(synth_with_blob_col):
    pgs = sgl_to_pgs("""
        visualize
            letter as x,
            number as y
        from synth
        collect by
            blob_col
        using lines
    """)
    layer = pgs["layers"][0]
    df = result_dfs(pgs, synth_with_blob_col)[0]

    with pytest.raises(SglError, match=re.escape(UNKNOWN_CLASS_MSG)):
        valid_column_classes(layer, df)
