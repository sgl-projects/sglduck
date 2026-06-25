"""Tests for valid_titles."""

import re

import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.validate import valid_titles


def untitled_aes_msg(aes):
    return (
        "Error: title provided for aesthetic not found"
        f" in any layer's aesthetic mapping: {aes}."
    )


def test_doesnt_raise_error_for_no_explicit_titles_with_single_layer():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x
        from cars
        using points
    """)

    valid_titles(pgs)


def test_doesnt_raise_error_for_no_explicit_titles_with_multiple_layers():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x
        from cars
        using points

        layer

        visualize
            hp as x
        from cars
        using points
    """)

    valid_titles(pgs)


def test_doesnt_raise_error_if_titled_aes_is_in_mapping():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x
        from cars
        using points
        title
            x as 'Miles Per Gallon'
    """)

    valid_titles(pgs)


def test_raises_error_if_titled_aes_is_not_in_mapping():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x
        from cars
        using points
        title
            y as 'Miles Per Gallon'
    """)

    with pytest.raises(SglError, match=re.escape(untitled_aes_msg("y"))):
        valid_titles(pgs)


def test_doesnt_raise_error_if_titled_aes_is_in_at_least_one_layers_mapping():
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
            mpg as y
        from cars
        using regression line

        title
            color as 'Cylinders'
    """)

    valid_titles(pgs)


def test_raises_error_if_titled_aes_is_not_in_any_layers_mapping():
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

        title
            color as 'Cylinders'
    """)

    with pytest.raises(SglError, match=re.escape(untitled_aes_msg("color"))):
        valid_titles(pgs)


def test_doesnt_raise_error_for_multiple_titled_aes_that_are_in_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
        title
            x as 'Horsepower',
            y as 'Miles Per Gallon'
    """)

    valid_titles(pgs)


def test_raises_error_if_one_titled_aes_is_not_in_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
        title
            x as 'Horsepower',
            y as 'Miles Per Gallon',
            color as 'Cylinders'
    """)

    with pytest.raises(SglError, match=re.escape(untitled_aes_msg("color"))):
        valid_titles(pgs)


def test_raises_error_if_multiple_titled_aes_are_not_in_mapping():
    pgs = sgl_to_pgs("""
        visualize
            mpg as x
        from cars
        using points
        title
            y as 'Miles Per Gallon',
            color as 'Cylinders'
    """)

    with pytest.raises(SglError, match=untitled_aes_msg("(y|color)")):
        valid_titles(pgs)


def test_doesnt_raise_error_for_multiple_titled_aes_in_some_layer_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points

        layer

        visualize
            mpg as y
        from cars
        using points

        title
            x as 'Horsepower',
            y as 'Miles Per Gallon'
    """)

    valid_titles(pgs)


def test_raises_error_if_one_titled_aes_is_not_in_any_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points

        layer

        visualize
            mpg as y
        from cars
        using points

        title
            x as 'Horsepower',
            y as 'Miles Per Gallon',
            color as 'Cylinders'
    """)

    with pytest.raises(SglError, match=re.escape(untitled_aes_msg("color"))):
        valid_titles(pgs)


def test_raises_error_if_multiple_titled_aes_are_not_in_any_mapping():
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points

        layer

        visualize
            mpg as x
        from cars
        using points

        title
            x as 'Horsepower',
            y as 'Miles Per Gallon',
            color as 'Cylinders'
    """)

    with pytest.raises(SglError, match=untitled_aes_msg("(y|color)")):
        valid_titles(pgs)
