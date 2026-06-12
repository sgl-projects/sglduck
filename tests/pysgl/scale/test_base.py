"""Tests for the SglScale base class."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs
from pysgl.scale import SglScale, SglScaleLinear


def test_base_is_instantiable():
    assert isinstance(SglScale(), SglScale)


def test_subclass_is_an_sgl_scale():
    assert isinstance(SglScaleLinear(), SglScale)


def test_valid_scale_raises_error_if_aes_not_in_any_layer(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape("Error: a scaled aesthetic must have at least one mapping"),
    ):
        SglScale().valid_scale("color", pgs["layers"], dfs)


def test_same_class_instances_are_equal_and_hash_alike():
    assert SglScale() == SglScale()
    assert hash(SglScale()) == hash(SglScale())


def test_different_classes_are_not_equal():
    assert SglScale() != SglScaleLinear()
