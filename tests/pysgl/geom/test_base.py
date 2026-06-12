"""Tests for the SglGeom base class (pure methods only).

``plotnine_aes`` requires a layer/DataFrame/scales and belongs to the rendering
milestone, so it is not ported here yet.
"""

from pysgl.geom import SglGeom, SglGeomPoint


def test_base_is_instantiable():
    assert isinstance(SglGeom(), SglGeom)


def test_subclass_is_an_sgl_geom():
    assert isinstance(SglGeomPoint(), SglGeom)


def test_geom_name_returns_geom():
    assert SglGeom().geom_name() == "geom"


def test_is_collective_returns_false():
    assert SglGeom().is_collective() is False


def test_same_class_instances_are_equal_and_hash_alike():
    assert SglGeom() == SglGeom()
    assert hash(SglGeom()) == hash(SglGeom())


def test_different_classes_are_not_equal():
    assert SglGeom() != SglGeomPoint()
