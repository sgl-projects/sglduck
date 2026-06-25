"""Tests for valid_aesthetics."""

import re

import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.validate import valid_aesthetics


def test_raises_error_for_no_positional_aes():
    pgs = sgl_to_pgs("""
        visualize
            mpg as color
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: positional mapping(s) must be provided, none were found."
        ),
    ):
        valid_aesthetics(layer)


@pytest.mark.parametrize("aes", ["x", "y", "theta", "r"])
def test_considers_single_positional_aes_valid(aes):
    pgs = sgl_to_pgs(f"""
        visualize
            mpg as {aes}
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_aesthetics(layer)


def test_considers_cartesian_coordinates_valid():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x,
            hp as y
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_aesthetics(layer)


def test_considers_polar_coordinates_valid():
    pgs = sgl_to_pgs("""
        visualize
            mpg as theta,
            hp as r
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_aesthetics(layer)


def test_raises_error_for_mixed_coordinate_systems():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x,
            hp as r
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: found aesthetics from multiple coordinate systems."
        " All positional aesthetics must be from a single coordinate system."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_aesthetics(layer)


def test_raises_error_for_more_than_two_positional_aes():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x,
            hp as y,
            cyl as theta
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: found aesthetics from multiple coordinate systems."
        " All positional aesthetics must be from a single coordinate system."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_aesthetics(layer)


def test_considers_valid_non_pos_aes_valid():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x,
            hp as y,
            cyl as color
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_aesthetics(layer)


def test_considers_invalid_non_pos_aes_invalid():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x,
            hp as y,
            cyl as size
        from cars
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: the size aesthetic is not valid for the line geom."
        ),
    ):
        valid_aesthetics(layer)
