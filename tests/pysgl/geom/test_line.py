"""Tests for SglGeomLine (pure methods only).

``group_aes_cols`` and ``plotnine_aes`` require a layer/DataFrame/scales and are
deferred to the rendering milestone.
"""

import plotnine

from pysgl.geom import SglGeom, SglGeomLine


def test_is_an_sgl_geom_line():
    assert isinstance(SglGeomLine(), SglGeomLine)
    assert isinstance(SglGeomLine(), SglGeom)


def test_geom_name_returns_line():
    assert SglGeomLine().geom_name() == "line"


def test_is_collective_returns_true():
    assert SglGeomLine().is_collective() is True


def test_extension_returns_two():
    assert SglGeomLine().extension() == 2


def test_plotnine_geom_returns_geom_line():
    assert SglGeomLine().plotnine_geom() is plotnine.geom_line


def test_has_direction_returns_true():
    assert SglGeomLine().has_direction() is True


def test_valid_qual_list_returns_direction_and_regression_quals():
    assert SglGeomLine().valid_qual_list() == ["horizontal", "regression", "vertical"]


def test_valid_non_pos_aes_returns_color():
    assert SglGeomLine().valid_non_pos_aes() == ["color"]
