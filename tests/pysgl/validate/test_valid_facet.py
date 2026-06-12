"""Tests for valid_facet."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs
from pysgl.validate import valid_facet

TWO_FACET_DIRECTION_MSG = (
    "Error: for two facets, one must be horizontal and the other vertical."
)

FACET_TYPE_PARAMS = [
    pytest.param("number", id="numerical"),
    pytest.param("day_and_time", id="temporal"),
    pytest.param("boolean", id="categorical"),
]


def assert_valid_facet_passes(sgl, con):
    pgs = sgl_to_pgs(sgl)
    dfs = result_dfs(pgs, con)

    valid_facet(pgs, dfs)


def test_doesnt_raise_error_for_no_faceting(test_con):
    assert_valid_facet_passes(
        """
        visualize
            day as x,
            number as y
        from synth
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize(
    "facet_clause",
    [
        pytest.param("boolean", id="default"),
        pytest.param("boolean horizontally", id="horizontal"),
        pytest.param("boolean vertically", id="vertical"),
        pytest.param("boolean, letter", id="two default"),
        pytest.param("boolean, letter horizontally", id="default + horizontal"),
        pytest.param("boolean, letter vertically", id="default + vertical"),
        pytest.param(
            "boolean horizontally, letter vertically",
            id="horizontal + vertical",
        ),
    ],
)
def test_doesnt_raise_error_for_valid_faceting(test_con, facet_clause):
    assert_valid_facet_passes(
        f"""
        visualize
            day as x,
            number as y
        from synth
        using points
        facet by
            {facet_clause}
        """,
        test_con,
    )


def test_raises_error_for_faceting_on_a_column_that_doesnt_exist(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x,
            number as y
        from synth
        using points
        facet by
            not_a_col
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: facet column 'not_a_col' does not exist in any layer data"
        " sources."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_facet(pgs, dfs)


@pytest.mark.parametrize("column_name", FACET_TYPE_PARAMS)
def test_doesnt_raise_error_due_to_facet_column_type(test_con, column_name):
    assert_valid_facet_passes(
        f"""
        visualize
            letter as x,
            day as y
        from synth
        using points
        facet by
            {column_name}
        """,
        test_con,
    )


@pytest.mark.parametrize("direction", ["horizontally", "vertically"])
def test_raises_error_for_two_facets_in_the_same_direction(test_con, direction):
    pgs = sgl_to_pgs(f"""
        visualize
            day as x,
            number as y
        from synth
        using points
        facet by
            letter {direction},
            boolean {direction}
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(TWO_FACET_DIRECTION_MSG)):
        valid_facet(pgs, dfs)


def test_raises_error_for_more_than_two_facets(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x,
            number as y
        from (
            select
                *,
                not boolean as boolean_opposite
            from synth
        )
        using points
        facet by
            letter,
            boolean,
            boolean_opposite
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError, match=re.escape("Error: cannot have more than two facets.")
    ):
        valid_facet(pgs, dfs)


@pytest.mark.parametrize("column_name", FACET_TYPE_PARAMS)
def test_doesnt_raise_error_for_valid_faceting_with_multiple_layers(
    test_con, column_name
):
    assert_valid_facet_passes(
        f"""
        visualize
            letter as x,
            day as y
        from synth
        using points

        layer

        visualize
            letter as x,
            day as y
        from synth
        using line

        facet by
            {column_name}
        """,
        test_con,
    )


@pytest.mark.parametrize(
    ("first_col", "second_col"),
    [
        pytest.param("number", "day_and_time", id="num and tmp"),
        pytest.param("number", "boolean", id="num and cat"),
        pytest.param("day_and_time", "boolean", id="tmp and cat"),
    ],
)
def test_raises_error_for_inconsistent_facet_column_type_across_layers(
    test_con, first_col, second_col
):
    pgs = sgl_to_pgs(f"""
        visualize
            letter as x,
            day as y
        from (
            select
                *,
                {first_col} as facet_col
            from synth
        )
        using points

        layer

        visualize
            letter as x,
            day as y
        from (
            select
                *,
                {second_col} as facet_col
            from synth
        )
        using points

        facet by
            facet_col
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: facet column 'facet_col' does not have a"
        " consistent type (categorical, numerical, or temporal)"
        " across all layers where it is present."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_facet(pgs, dfs)


def test_raises_error_if_facet_col_has_unknown_type_class(synth_with_blob_col):
    pgs = sgl_to_pgs("""
        visualize
            letter as x,
            number as y
        from synth
        using line

        facet by
            blob_col
    """)
    dfs = result_dfs(pgs, synth_with_blob_col)

    expected_msg = (
        "Error: unknown SGL type classification"
        " (numerical, categorical, or temporal)"
        " for column 'blob_col'."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_facet(pgs, dfs)


def test_raises_error_for_invalid_faceting_with_multiple_layers(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x,
            number as y
        from synth
        using points

        layer

        visualize
            day as x,
            number_plus_one as y
        from (
            select
                *,
                number + 1 as number_plus_one
            from synth
        )
        using points

        facet by
            letter horizontally,
            boolean horizontally
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(TWO_FACET_DIRECTION_MSG)):
        valid_facet(pgs, dfs)


def test_doesnt_raise_error_if_facet_column_exists_in_some_layers_only(test_con):
    assert_valid_facet_passes(
        """
        visualize
            day as x,
            number as y
        from synth
        using points

        layer

        visualize
            day as x,
            number as y
        from (
            select
                day,
                number
            from synth
        )
        using points

        facet by
            boolean
        """,
        test_con,
    )
