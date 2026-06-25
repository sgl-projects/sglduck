"""Tests for valid_qualifier and valid_box_direction."""

import re

import pytest

from sglduck import SglError
from sglduck.constants import CART_AES, POLAR_AES
from sglduck.pgs import sgl_to_pgs
from sglduck.validate import valid_box_direction, valid_qualifier

ALIGNED_DIRS = {
    "x": "horizontal",
    "y": "vertical",
    "theta": "horizontal",
    "r": "vertical",
}
UNALIGNED_DIRS = {
    "x": "vertical",
    "y": "horizontal",
    "theta": "vertical",
    "r": "horizontal",
}


def other_pos_aes(aes):
    coords = CART_AES if aes in CART_AES else POLAR_AES
    return next(other for other in coords if other != aes)


@pytest.mark.parametrize("aes", list(ALIGNED_DIRS))
def test_box_direction_allows_aligned_single_pos_aes(aes):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes}
        from cars
        using {ALIGNED_DIRS[aes]} box
    """)
    layer = pgs["layers"][0]

    valid_box_direction(layer)


@pytest.mark.parametrize("aes", list(UNALIGNED_DIRS))
def test_box_direction_raises_error_for_unaligned_single_pos_aes(aes):
    direction = UNALIGNED_DIRS[aes]
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes}
        from cars
        using {direction} box
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: a single positional aesthetic"
        f" of {aes} does not align with the {direction} qualifier"
        " for the box geom."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_box_direction(layer)


@pytest.mark.parametrize("direction", ["horizontal", "vertical"])
def test_box_direction_allows_two_pos_aes_without_collection(direction):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as x,
            mpg as y
        from cars
        using {direction} boxes
    """)
    layer = pgs["layers"][0]

    valid_box_direction(layer)


@pytest.mark.parametrize("direction", ["horizontal", "vertical"])
def test_box_direction_allows_collection_without_pos_aes_mappings(direction):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            cyl
        using {direction} boxes
    """)
    layer = pgs["layers"][0]

    valid_box_direction(layer)


@pytest.mark.parametrize("direction", ["horizontal", "vertical"])
def test_box_direction_allows_collection_with_both_pos_aes_mappings(direction):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            hp,
            mpg
        using {direction} boxes
    """)
    layer = pgs["layers"][0]

    valid_box_direction(layer)


@pytest.mark.parametrize("aes", list(ALIGNED_DIRS))
def test_box_direction_allows_aligned_uncollected_pos_aes(aes):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes},
            mpg as {other_pos_aes(aes)}
        from cars
        collect by
            mpg
        using {ALIGNED_DIRS[aes]} boxes
    """)
    layer = pgs["layers"][0]

    valid_box_direction(layer)


@pytest.mark.parametrize("aes", list(UNALIGNED_DIRS))
def test_box_direction_raises_error_for_unaligned_uncollected_pos_aes(aes):
    direction = UNALIGNED_DIRS[aes]
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes},
            mpg as {other_pos_aes(aes)}
        from cars
        collect by
            mpg
        using {direction} boxes
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: a single uncollected positional aesthetic"
        f" of {aes} does not align with the {direction} qualifier"
        " for the box geom."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_box_direction(layer)


def test_qualifier_considers_default_valid():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    layer = pgs["layers"][0]

    valid_qualifier(layer)


def test_qualifier_considers_valid_qualifier_valid():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using jittered points
    """)
    layer = pgs["layers"][0]

    valid_qualifier(layer)


def test_qualifier_considers_invalid_qualifier_invalid():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using regression boxes
    """)
    layer = pgs["layers"][0]

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: the regression qualifier is not valid for the box geom."
        ),
    ):
        valid_qualifier(layer)


def test_qualifier_performs_additional_checks_for_box_direction():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            hp
        using horizontal boxes
    """)
    layer = pgs["layers"][0]

    expected_msg = (
        "Error: a single uncollected positional aesthetic"
        " of y does not align with the horizontal qualifier"
        " for the box geom."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_qualifier(layer)


def test_qualifier_doesnt_perform_additional_checks_for_non_box():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        collect by
            hp
        using horizontal lines
    """)
    layer = pgs["layers"][0]

    valid_qualifier(layer)
