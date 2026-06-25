"""Tests for titles (port of test-titles.R).

rsgl asserts against the ggplot2 labels object (`actual_labs$x`, `$colour`,
`$fill`); the analog here asserts against `labs_args(pgs)`, the aes -> title dict
that `lets_plot_labs` feeds to `lets_plot.labs`. The non-bar color legend key is
`color` (lets-plot) where rsgl/ggplot2 use `colour`. A few integration checks go
through `lets_plot_labs` and read the resulting plot's `guides` spec.
"""

import lets_plot
import pytest

from sglduck.pgs import sgl_to_pgs
from sglduck.titles import labs_args, lets_plot_labs, title_for_aes

# Default-title cases shared with rsgl's default_title_cases().
DEFAULT_TITLE_EXPRS = ["mpg", "bin(mpg)", "count(*)"]

# (geom, other_geom, expected color key, unexpected color key); rsgl's color_cases().
COLOR_CASES = [
    ("bars", "points", "fill", "color"),
    ("points", "bars", "color", "fill"),
]


# --- title_for_aes -----------------------------------------------------------

def test_title_for_aes_returns_explicit_title():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using points
        title x as 'Horsepower', y as 'Miles Per Gallon'
        """
    )
    assert title_for_aes("x", pgs) == "Horsepower"


def test_title_for_aes_returns_default_from_first_layer_with_aes():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using line
        layer
        visualize hp as x, mpg as y, bin(cyl) as color from cars using points
        layer
        visualize hp as x, mpg as y, wt as color from cars using points
        title x as 'Horsepower', y as 'Miles Per Gallon'
        """
    )
    assert title_for_aes("color", pgs) == "bin(cyl)"


# --- labs_args: positional / non-color aesthetics ----------------------------

def test_labs_args_uses_explicit_title():
    pgs = sgl_to_pgs(
        "visualize mpg as x from cars using points title x as 'Miles Per Gallon'"
    )
    assert labs_args(pgs)["x"] == "Miles Per Gallon"


@pytest.mark.parametrize("expr", DEFAULT_TITLE_EXPRS)
def test_labs_args_uses_default_title(expr):
    pgs = sgl_to_pgs(f"visualize {expr} as x from cars using points")
    assert labs_args(pgs)["x"] == expr


def test_labs_args_skips_layer_without_aes():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using regression line
        layer
        visualize hp as x, mpg as y, cyl as color from cars using points
        """
    )
    assert labs_args(pgs)["color"] == "cyl"


def test_labs_args_uses_title_from_first_layer_when_present_in_multiple():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using points
        layer
        visualize bin(hp) as x, count(*) as y from cars using bars
        """
    )
    assert labs_args(pgs)["x"] == "hp"


@pytest.mark.parametrize("aes", ["x", "y", "size"])
def test_labs_args_key_matches_aes_name(aes):
    other_aes = "y" if aes == "x" else "x"
    pgs = sgl_to_pgs(
        f"visualize hp as {other_aes}, mpg as {aes} from cars using points"
    )
    assert labs_args(pgs)[aes] == "mpg"


@pytest.mark.parametrize("aes,expected_key", [("theta", "x"), ("r", "y")])
def test_labs_args_polar_positional_aes_folds_onto_cartesian_key(aes, expected_key):
    pgs = sgl_to_pgs(f"visualize mpg as {aes} from cars using points")
    args = labs_args(pgs)
    assert args[expected_key] == "mpg"
    assert aes not in args


# --- labs_args: color aesthetic (fill for bars, color otherwise) -------------

@pytest.mark.parametrize("geom,_other,expected_key,unexpected_key", COLOR_CASES)
def test_labs_args_explicit_color_title(geom, _other, expected_key, unexpected_key):
    pgs = sgl_to_pgs(
        f"visualize mpg as color from cars using {geom}"
        " title color as 'Miles Per Gallon'"
    )
    args = labs_args(pgs)
    assert args[expected_key] == "Miles Per Gallon"
    assert unexpected_key not in args


@pytest.mark.parametrize("geom,_other,expected_key,unexpected_key", COLOR_CASES)
@pytest.mark.parametrize("expr", DEFAULT_TITLE_EXPRS)
def test_labs_args_default_color_title(geom, _other, expected_key, unexpected_key, expr):
    pgs = sgl_to_pgs(f"visualize {expr} as color from cars using {geom}")
    args = labs_args(pgs)
    assert args[expected_key] == expr
    assert unexpected_key not in args


@pytest.mark.parametrize("geom,_other,expected_key,unexpected_key", COLOR_CASES)
def test_labs_args_skips_layer_without_color_aes(geom, _other, expected_key, unexpected_key):
    pgs = sgl_to_pgs(
        f"""
        visualize hp as x, mpg as y from cars using {geom}
        layer
        visualize hp as x, mpg as y, cyl as color from cars using {geom}
        """
    )
    args = labs_args(pgs)
    assert args[expected_key] == "cyl"
    assert unexpected_key not in args


@pytest.mark.parametrize("geom,_other,expected_key,unexpected_key", COLOR_CASES)
def test_labs_args_color_title_from_first_layer_when_present_in_multiple(
    geom, _other, expected_key, unexpected_key
):
    pgs = sgl_to_pgs(
        f"""
        visualize hp as color from cars using {geom}
        layer
        visualize bin(hp) as color from cars using {geom}
        """
    )
    args = labs_args(pgs)
    assert args[expected_key] == "hp"
    assert unexpected_key not in args


@pytest.mark.parametrize("geom,other,expected_key,unexpected_key", COLOR_CASES)
def test_labs_args_picks_key_by_layer_with_color_mapping(
    geom, other, expected_key, unexpected_key
):
    # color is mapped only on the first (geom) layer; the second (other) layer
    # has no color mapping, so the key follows the color-mapped layer's geom.
    pgs = sgl_to_pgs(
        f"""
        visualize hp as x, mpg as y, cyl as color from cars using {geom}
        layer
        visualize hp as x, mpg as y from cars using {other}
        """
    )
    args = labs_args(pgs)
    assert args[expected_key] == "cyl"
    assert unexpected_key not in args


def test_labs_args_returns_both_fill_and_color_for_bar_and_non_bar():
    pgs = sgl_to_pgs(
        """
        visualize bin(carat) as x, count(*) as y, cut as color from diamonds
        group by bin(carat), cut using bars
        layer
        visualize carat as x, price as y, clarity as color from diamonds using points
        """
    )
    args = labs_args(pgs)
    assert args["fill"] == "cut"
    assert args["color"] == "clarity"


def test_labs_args_returns_first_instances_of_fill_and_color():
    pgs = sgl_to_pgs(
        """
        visualize bin(carat) as x, count(*) as y, cut as color from diamonds
        group by bin(carat), cut using bars
        layer
        visualize bin(carat) as x, count(*) as y, clarity as color from diamonds
        group by bin(carat), clarity using bars
        layer
        visualize carat as x, price as y, clarity as color from diamonds using points
        layer
        visualize carat as x, price as y, cut as color from diamonds using points
        """
    )
    args = labs_args(pgs)
    assert args["fill"] == "cut"
    assert args["color"] == "clarity"


def test_labs_args_returns_titles_for_multiple_aes():
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y from cars using line
        layer
        visualize hp as x, mpg as y, cyl as color from cars using points
        title y as 'Miles Per Gallon'
        """
    )
    args = labs_args(pgs)
    assert set(args) == {"x", "y", "color"}
    assert args["x"] == "hp"
    assert args["y"] == "Miles Per Gallon"
    assert args["color"] == "cyl"


# --- lets_plot_labs integration (label text lands in the plot's guides) -------

def test_lets_plot_labs_sets_axis_guide_titles():
    pgs = sgl_to_pgs(
        "visualize hp as x, mpg as y from cars using points title x as 'Horsepower'"
    )
    guides = (lets_plot.ggplot() + lets_plot_labs(pgs)).as_dict()["guides"]
    assert guides["x"]["title"] == "Horsepower"
    assert guides["y"]["title"] == "mpg"


def test_lets_plot_labs_routes_bar_color_to_fill_guide():
    pgs = sgl_to_pgs(
        "visualize mpg as color from cars using bars title color as 'Miles Per Gallon'"
    )
    guides = (lets_plot.ggplot() + lets_plot_labs(pgs)).as_dict()["guides"]
    assert guides["fill"]["title"] == "Miles Per Gallon"
    assert "color" not in guides
