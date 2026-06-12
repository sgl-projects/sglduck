"""Tests for valid_scales."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs
from pysgl.validate import valid_scales


def test_doesnt_raise_error_for_default_scales(test_con):
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
    """)
    dfs = result_dfs(pgs, test_con)

    valid_scales(pgs, dfs)


def test_doesnt_raise_error_for_valid_explicit_scales(test_con):
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

        scale by
            linear(x),
            log(color)
    """)
    dfs = result_dfs(pgs, test_con)

    valid_scales(pgs, dfs)


def test_raises_error_for_invalid_explicit_scale(test_con):
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

        scale by
            linear(x),
            log(color)
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape("Error: a scaled aesthetic must have at least one mapping"),
    ):
        valid_scales(pgs, dfs)
