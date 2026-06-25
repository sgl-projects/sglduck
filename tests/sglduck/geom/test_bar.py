"""Tests for SglGeomBar (pure methods only).

``lets_plot_aes`` (including the colour -> fill remap) is deferred to the
rendering milestone.
"""

import lets_plot

from sglduck.geom import SglGeom, SglGeomBar


def test_is_an_sgl_geom_bar():
    assert isinstance(SglGeomBar(), SglGeomBar)
    assert isinstance(SglGeomBar(), SglGeom)


def test_geom_name_returns_bar():
    assert SglGeomBar().geom_name() == "bar"


def test_is_collective_returns_false():
    assert SglGeomBar().is_collective() is False


def test_lets_plot_geom_returns_geom_bar():
    assert SglGeomBar().lets_plot_geom() is lets_plot.geom_bar


def test_has_direction_returns_true():
    assert SglGeomBar().has_direction() is True


def test_valid_qual_list_returns_direction_quals():
    assert SglGeomBar().valid_qual_list() == ["horizontal", "unstacked", "vertical"]


def test_valid_non_pos_aes_returns_color():
    assert SglGeomBar().valid_non_pos_aes() == ["color"]
