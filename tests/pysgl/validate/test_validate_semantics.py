"""Tests for validate_semantics."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs
from pysgl.validate import validate_semantics


def test_doesnt_raise_error_for_valid_semantics(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    validate_semantics(pgs, dfs)


def test_raises_error_if_column_name_doesnt_exist(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            not_a_col as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape("Error: referenced column 'not_a_col' not found"),
    ):
        validate_semantics(pgs, dfs)


def test_raises_error_if_column_class_is_invalid(synth_with_blob_col):
    pgs = sgl_to_pgs("""
        visualize
            blob_col as x,
            number as y
        from synth
        using points
    """)
    dfs = result_dfs(pgs, synth_with_blob_col)

    expected_msg = (
        "Error: unknown SGL type classification"
        " (numerical, categorical, or temporal)"
        " for column 'blob_col'."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_cta(test_con):
    pgs = sgl_to_pgs("""
        visualize
            bin(letter) as x,
            count(*) as y
        from synth
        group by
            bin(letter)
        using bars
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: cannot apply bin to a categorical column, found bin(letter)."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_aesthetics(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as theta
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: found aesthetics from multiple coordinate systems."
        " All positional aesthetics must be from a single coordinate system."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_qualifier(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using jittered bars
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: the jittered qualifier is not valid for the bar geom."
        ),
    ):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_groupings(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        group by
            hp
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: unaggregated expressions in the visualize"
        " and collect by clauses must also be present in the"
        " group by clause."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_collections(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cut as x,
            price as y,
            clarity as color
        from diamonds
        collect by
            cut
        using boxes
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: all expressions mapped to from non-positional"
        " aesthetics must be included in the collect by clause."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_doesnt_raise_error_for_multiple_layers_with_valid_semantics(test_con):
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
        from cars
        using regression line
    """)
    dfs = result_dfs(pgs, test_con)

    validate_semantics(pgs, dfs)


def test_raises_error_given_multiple_layers_where_a_layer_is_invalid(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points

        layer

        visualize
            number as x,
            letter as y
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: an aesthetic must be mapped to the same type"
        " (numerical, categorical, or temporal) across layers."
        " Found the following types for the y aesthetic: numerical, categorical."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_scaling(test_con):
    pgs = sgl_to_pgs("""
        visualize
            letter as x,
            number as y
        from synth
        using points
        scale by
            log(x)
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: the log scale can only be applied"
        " to aesthetics with numerical mappings."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_faceting(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
        facet by
            cyl,
            vs,
            am
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError, match=re.escape("Error: cannot have more than two facets.")
    ):
        validate_semantics(pgs, dfs)


def test_raises_error_for_invalid_title(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
        title
            color as 'Cylinders'
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: title provided for aesthetic not found"
        " in any layer's aesthetic mapping: color."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        validate_semantics(pgs, dfs)
