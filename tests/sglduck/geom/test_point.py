"""Tests for SglGeomPoint (pure methods only).

``lets_plot_aes`` is deferred to the rendering milestone.
"""

import lets_plot

from sglduck.geom import SglGeom, SglGeomPoint


def test_is_an_sgl_geom_point():
    assert isinstance(SglGeomPoint(), SglGeomPoint)
    assert isinstance(SglGeomPoint(), SglGeom)


def test_geom_name_returns_point():
    assert SglGeomPoint().geom_name() == "point"


def test_is_collective_returns_false():
    assert SglGeomPoint().is_collective() is False


def test_lets_plot_geom_returns_geom_point():
    assert SglGeomPoint().lets_plot_geom() is lets_plot.geom_point


def test_has_direction_returns_false():
    assert SglGeomPoint().has_direction() is False


def test_valid_qual_list_returns_jittered():
    assert SglGeomPoint().valid_qual_list() == ["jittered"]


def test_valid_non_pos_aes_returns_color_and_size():
    assert SglGeomPoint().valid_non_pos_aes() == ["color", "size"]
