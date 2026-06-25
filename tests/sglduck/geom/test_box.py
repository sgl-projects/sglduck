"""Tests for SglGeomBox (pure methods only).

``group_aes_cols`` and ``lets_plot_aes`` require a layer/DataFrame/scales and are
deferred to the rendering milestone.
"""

import lets_plot

from sglduck.geom import SglGeom, SglGeomBox


def test_is_an_sgl_geom_box():
    assert isinstance(SglGeomBox(), SglGeomBox)
    assert isinstance(SglGeomBox(), SglGeom)


def test_geom_name_returns_box():
    assert SglGeomBox().geom_name() == "box"


def test_is_collective_returns_true():
    assert SglGeomBox().is_collective() is True


def test_extension_returns_one():
    assert SglGeomBox().extension() == 1


def test_lets_plot_geom_returns_geom_boxplot():
    assert SglGeomBox().lets_plot_geom() is lets_plot.geom_boxplot


def test_has_direction_returns_true():
    assert SglGeomBox().has_direction() is True


def test_valid_qual_list_returns_direction_quals():
    assert SglGeomBox().valid_qual_list() == ["horizontal", "vertical"]


def test_valid_non_pos_aes_returns_color():
    assert SglGeomBox().valid_non_pos_aes() == ["color"]
