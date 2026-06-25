"""Render tests for SglPlot (slice of test-sgl_plot.R).

rsgl uses vdiffr SVG snapshot baselines; choosing and wiring up an equivalent
lets-plot snapshot tool is a follow-up (plan section 14). For now these are
smoke tests: a SglPlot renders to non-empty SVG/HTML through the full
cast_columns -> perform_ctas -> rgs_to_lets_plot pipeline.
"""

from sglduck import db_get_plot

SCATTERPLOT_STMT = """
    visualize
      hp as x,
      mpg as y
    from cars
    using points
"""


def test_renders_svg(test_con):
    svg = db_get_plot(test_con, SCATTERPLOT_STMT).to_svg()
    assert "<svg" in svg


def test_renders_html(test_con):
    html = db_get_plot(test_con, SCATTERPLOT_STMT).to_html()
    assert "<html" in html.lower() or "<div" in html.lower()
