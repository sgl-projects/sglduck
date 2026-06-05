"""Port of rsgl's test-sgl_geom_box.R (pure methods only).

``group_aes_cols`` and ``plotnine_aes`` require a layer/DataFrame/scales and are
deferred to the rendering milestone.
"""

import plotnine

from pysgl.geom import SglGeom, SglGeomBox


def test_is_an_sgl_geom_box():
    assert isinstance(SglGeomBox(), SglGeomBox)
    assert isinstance(SglGeomBox(), SglGeom)


def test_geom_name_returns_box():
    assert SglGeomBox().geom_name() == "box"


def test_is_collective_returns_true():
    assert SglGeomBox().is_collective() is True


def test_plotnine_geom_returns_geom_boxplot():
    assert SglGeomBox().plotnine_geom() is plotnine.geom_boxplot


def test_has_direction_returns_true():
    assert SglGeomBox().has_direction() is True
