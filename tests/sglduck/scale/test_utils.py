"""Tests for the scale rendering helpers (port of the rendering part of
test-sgl_scale_utils.R: lets_plot_color_aes and lets_plot_continuous_scales).

Scale features are compared by their ``as_dict()`` against the same lets-plot
constructors the helpers dispatch to.
"""

import lets_plot
import pytest

from sglduck.pgs import sgl_to_pgs
from sglduck.scale.utils import lets_plot_color_aes, lets_plot_continuous_scales


def _as_dicts(scales):
    return [scale.as_dict() for scale in scales]


# --- lets_plot_color_aes -----------------------------------------------------

def test_color_aes_empty_when_no_color_mapping():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using points
        layer
        visualize hp as x, mpg as y from cars using bars
        """
    )
    assert lets_plot_color_aes(pgs) == []


def test_color_aes_is_color_for_non_bar():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y from cars using bars
        """
    )
    assert lets_plot_color_aes(pgs) == ["color"]


def test_color_aes_is_fill_for_bar():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using bars
        """
    )
    assert lets_plot_color_aes(pgs) == ["fill"]


def test_color_aes_is_both_for_bar_and_non_bar():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using bars
        """
    )
    assert set(lets_plot_color_aes(pgs)) == {"color", "fill"}


def test_color_aes_has_no_duplicates():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using line
        """
    )
    assert lets_plot_color_aes(pgs) == ["color"]


# --- lets_plot_continuous_scales: non-color aesthetics -----------------------

@pytest.mark.parametrize("transform", ["identity", "log10"])
@pytest.mark.parametrize(
    "aes,scale_ctor",
    [
        ("x", lets_plot.scale_x_continuous),
        ("y", lets_plot.scale_y_continuous),
        ("theta", lets_plot.scale_x_continuous),
        ("r", lets_plot.scale_y_continuous),
        ("size", lets_plot.scale_size),
    ],
)
def test_continuous_scales_for_non_color_aes(aes, scale_ctor, transform):
    pgs = sgl_to_pgs(f"visualize hp as {aes} from cars using points")
    assert _as_dicts(lets_plot_continuous_scales(transform, aes, pgs)) == _as_dicts(
        [scale_ctor(trans=transform)]
    )


# --- lets_plot_continuous_scales: color aesthetic ----------------------------

def test_continuous_scales_color_for_non_bar():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y from cars using bars
        """
    )
    assert _as_dicts(
        lets_plot_continuous_scales("identity", "color", pgs)
    ) == _as_dicts([lets_plot.scale_color_continuous(trans="identity")])


def test_continuous_scales_fill_for_bar():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using bars
        """
    )
    assert _as_dicts(
        lets_plot_continuous_scales("identity", "color", pgs)
    ) == _as_dicts([lets_plot.scale_fill_continuous(trans="identity")])


def test_continuous_scales_color_and_fill_for_both():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using bars
        """
    )
    by_aes = {
        scale.as_dict()["aesthetic"]: scale.as_dict()
        for scale in lets_plot_continuous_scales("identity", "color", pgs)
    }
    assert set(by_aes) == {"color", "fill"}
    assert all(d["trans"] == "identity" for d in by_aes.values())


def test_continuous_scales_color_has_no_duplicates():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        layer
        visualize hp as x, mpg as y, cyl as color from cars using line
        """
    )
    assert _as_dicts(
        lets_plot_continuous_scales("identity", "color", pgs)
    ) == _as_dicts([lets_plot.scale_color_continuous(trans="identity")])
