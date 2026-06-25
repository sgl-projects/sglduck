"""Tests for valid_layering."""

import re

import pytest

from sglduck import SglError
from sglduck.constants import CART_AES, POLAR_AES, POS_AES
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.validate import valid_layering


def two_layer_stmt(layer_1_expr, layer_1_source, layer_2_expr, layer_2_source):
    return f"""
        visualize
            {layer_1_expr} as x
        from {layer_1_source}
        using points

        layer

        visualize
            {layer_2_expr} as x
        from {layer_2_source}
        using points
    """


def test_single_layer_is_valid(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    valid_layering(pgs, dfs)


@pytest.mark.parametrize(
    ("layer_1_source", "layer_1_expr", "layer_2_source", "layer_2_expr"),
    [
        pytest.param("cars", "hp", "synth", "number", id="both numerical"),
        pytest.param("cars", "hp", "synth", "count(*)", id="numerical and count"),
        pytest.param("diamonds", "color", "synth", "letter", id="both categorical"),
        pytest.param(
            "synth", "day_and_time", "economics", "date", id="both temporal"
        ),
        pytest.param("cars", "hp", "cars", "bin(mpg)", id="bin of same type"),
    ],
)
def test_layering_of_compatible_types_is_valid(
    test_con, layer_1_source, layer_1_expr, layer_2_source, layer_2_expr
):
    pgs = sgl_to_pgs(
        two_layer_stmt(layer_1_expr, layer_1_source, layer_2_expr, layer_2_source)
    )
    dfs = result_dfs(pgs, test_con)

    valid_layering(pgs, dfs)


@pytest.mark.parametrize(
    ("layer_1_source", "layer_1_expr", "layer_2_source", "layer_2_expr"),
    [
        pytest.param("cars", "hp", "synth", "letter", id="num and cat"),
        pytest.param("cars", "hp", "synth", "day", id="num and temp"),
        pytest.param("synth", "letter", "synth", "day_and_time", id="cat and temp"),
    ],
)
def test_layering_of_incompatible_types_is_invalid(
    test_con, layer_1_source, layer_1_expr, layer_2_source, layer_2_expr
):
    pgs = sgl_to_pgs(
        two_layer_stmt(layer_1_expr, layer_1_source, layer_2_expr, layer_2_source)
    )
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError):
        valid_layering(pgs, dfs)


def test_incompatible_type_layering_gives_correct_error_message(test_con):
    pgs = sgl_to_pgs(two_layer_stmt("hp", "cars", "letter", "synth"))
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: an aesthetic must be mapped to the same type"
        " (numerical, categorical, or temporal) across layers."
        " Found the following types for the x aesthetic: numerical, categorical."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_layering(pgs, dfs)


@pytest.mark.parametrize("aes", ["y", "theta", "r", "color"])
def test_no_error_is_raised_for_valid_layering_of_other_aesthetics(test_con, aes):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes}
        from cars
        using points

        layer

        visualize
            number as {aes}
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    valid_layering(pgs, dfs)


@pytest.mark.parametrize("aes", ["y", "theta", "r", "color"])
def test_error_is_raised_for_invalid_layering_of_other_aesthetics(test_con, aes):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {aes}
        from cars
        using points

        layer

        visualize
            letter as {aes}
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError):
        valid_layering(pgs, dfs)


@pytest.mark.parametrize("aes", ["color", "size"])
def test_no_error_is_raised_for_non_positional_aes_in_one_layer_only(
    test_con, aes
):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as x,
            mpg as y,
            cyl as {aes}
        from cars
        using points

        layer

        visualize
            pop as x,
            unemploy as y
        from economics
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    valid_layering(pgs, dfs)


@pytest.mark.parametrize(
    "coords",
    [
        pytest.param(CART_AES, id="cartesian"),
        pytest.param(POLAR_AES, id="polar"),
    ],
)
def test_no_error_is_raised_for_consistent_coordinates_across_layers(
    test_con, coords
):
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {coords[0]},
            mpg as {coords[1]},
            cyl as color
        from cars
        using points

        layer

        visualize
            hp as {coords[0]},
            mpg as {coords[1]}
        from cars
        using regression line
    """)
    dfs = result_dfs(pgs, test_con)

    valid_layering(pgs, dfs)


@pytest.mark.parametrize("test_aes", POS_AES)
def test_error_is_raised_if_positional_aes_inconsistent_across_layers(
    test_con, test_aes
):
    different_aes = next(aes for aes in POS_AES if aes != test_aes)
    pgs = sgl_to_pgs(f"""
        visualize
            hp as {test_aes}
        from cars
        using points

        layer

        visualize
            mpg as {different_aes}
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    expected_msg = (
        "Error: if a positional aesthetic is present in one layer,"
        f" it must be present in all layers. '{test_aes}' is not present in"
        " all layers."
    )
    with pytest.raises(SglError, match=re.escape(expected_msg)):
        valid_layering(pgs, dfs)
