"""Tests for the SglScale base class (pure methods only).

``valid_scale`` requires layers and DataFrames and belongs to the validation
milestone, so it is not ported here yet.
"""

from pysgl.scale import SglScale, SglScaleLinear


def test_base_is_instantiable():
    assert isinstance(SglScale(), SglScale)


def test_subclass_is_an_sgl_scale():
    assert isinstance(SglScaleLinear(), SglScale)


def test_scale_name_returns_base():
    assert SglScale().scale_name() == "base"


def test_same_class_instances_are_equal_and_hash_alike():
    assert SglScale() == SglScale()
    assert hash(SglScale()) == hash(SglScale())


def test_different_classes_are_not_equal():
    assert SglScale() != SglScaleLinear()
