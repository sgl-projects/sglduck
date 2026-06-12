"""Tests for valid_collections."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.validate import valid_collections


def test_doesnt_raise_error_if_collect_by_omitted_for_collective_geom():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using line
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_doesnt_raise_error_if_collect_by_omitted_for_non_collective_geom():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_raises_error_for_collect_by_with_non_collective_geom():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            cyl
        using points
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: collect by clause should not be provided"
        " for non-collective geom point."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_collections(layer)


def test_doesnt_raise_error_if_non_pos_aes_exprs_are_proper_subset():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_doesnt_raise_error_if_non_pos_aes_exprs_are_same_as_collections():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y,
            cyl as color
        from cars
        collect by
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_raises_error_if_non_pos_aes_exprs_are_not_subset_of_collections():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y,
            cyl as color,
            am as size
        from cars
        collect by
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: all expressions mapped to from non-positional"
        " aesthetics must be included in the collect by clause."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_collections(layer)


def test_doesnt_raise_error_if_uncollected_pos_count_below_extension():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            hp,
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_doesnt_raise_error_if_uncollected_pos_count_equals_extension():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    valid_collections(layer)


def test_raises_error_if_uncollected_pos_count_exceeds_extension():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            cyl
        using boxes
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: the number of uncollected positional aesthetic"
        " expressions exceeds the extensionality of the box geom."
        " Add an expression mapped to from a positional aesthetic"
        " to the collect by clause."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_collections(layer)
