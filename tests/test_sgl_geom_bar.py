"""Port of rsgl's test-sgl_geom_bar.R (pure methods only).

``plotnine_aes`` (including the colour -> fill remap) is deferred to the
rendering milestone.
"""

import plotnine

from pysgl.geom import SglGeom, SglGeomBar


def test_is_an_sgl_geom_bar():
    assert isinstance(SglGeomBar(), SglGeomBar)
    assert isinstance(SglGeomBar(), SglGeom)


def test_geom_name_returns_bar():
    assert SglGeomBar().geom_name() == "bar"


def test_is_collective_returns_false():
    assert SglGeomBar().is_collective() is False


def test_plotnine_geom_returns_geom_bar():
    assert SglGeomBar().plotnine_geom() is plotnine.geom_bar


def test_has_direction_returns_true():
    assert SglGeomBar().has_direction() is True
