"""Port of rsgl's test-sgl_geom_point.R (pure methods only).

``plotnine_aes`` is deferred to the rendering milestone.
"""

import plotnine

from pysgl.geom import SglGeom, SglGeomPoint


def test_is_an_sgl_geom_point():
    assert isinstance(SglGeomPoint(), SglGeomPoint)
    assert isinstance(SglGeomPoint(), SglGeom)


def test_geom_name_returns_point():
    assert SglGeomPoint().geom_name() == "point"


def test_is_collective_returns_false():
    assert SglGeomPoint().is_collective() is False


def test_plotnine_geom_returns_geom_point():
    assert SglGeomPoint().plotnine_geom() is plotnine.geom_point


def test_has_direction_returns_false():
    assert SglGeomPoint().has_direction() is False
