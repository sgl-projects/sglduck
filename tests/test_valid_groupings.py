"""Tests for valid_groupings."""

import re

import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.validate import valid_groupings

UNGROUPED_UNAGGS_MSG = (
    "Error: unaggregated expressions in the visualize"
    " and collect by clauses must also be present in the"
    " group by clause."
)
NO_GROUP_BY_MSG = (
    "Error: given that aggregations are present,"
    " all unaggregated expressions in the visualize"
    " and collect by clause must also be included"
    " in the group by clause."
    " However, no group by clause was provided."
)


def test_doesnt_raise_error_if_viz_collect_unaggs_are_proper_subset():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x
        from cars
        group by
            bin(mpg),
            hp
        collect by
            bin(mpg)
        using lines
    """)
    layer = pgs["layers"][0]

    valid_groupings(layer)


def test_doesnt_raise_error_if_viz_collect_unaggs_are_same_as_groupings():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y
        from cars
        group by
            bin(mpg),
            hp
        collect by
            bin(mpg),
            hp
        using lines
    """)
    layer = pgs["layers"][0]

    valid_groupings(layer)


def test_raises_error_if_viz_unaggs_are_not_subset_of_groupings():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y,
            cyl as color
        from cars
        group by
            bin(mpg),
            hp
        collect by
            bin(mpg),
            hp
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(SglError, match=re.escape(UNGROUPED_UNAGGS_MSG)):
        valid_groupings(layer)


def test_raises_error_if_collect_unaggs_are_not_subset_of_groupings():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y
        from cars
        group by
            bin(mpg),
            hp
        collect by
            bin(mpg),
            hp,
            cyl
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(SglError, match=re.escape(UNGROUPED_UNAGGS_MSG)):
        valid_groupings(layer)


def test_ignores_aggregated_expressions_in_viz_and_collect_clauses():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y,
            count(*) as color
        from cars
        group by
            bin(mpg),
            hp
        collect by
            bin(mpg),
            hp,
            count(*)
        using lines
    """)
    layer = pgs["layers"][0]

    valid_groupings(layer)


def test_raises_error_for_aggregation_in_group_by_clause():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y,
            avg(cyl) as color
        from cars
        group by
            bin(mpg),
            hp,
            avg(cyl)
        collect by
            bin(mpg),
            hp,
            avg(cyl)
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: group by clause cannot contain aggregation expressions."
        ),
    ):
        valid_groupings(layer)


def test_doesnt_raise_error_if_group_by_omitted_without_aggregations():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            hp as y
        from cars
        collect by
            bin(mpg),
            hp
        using lines
    """)
    layer = pgs["layers"][0]

    valid_groupings(layer)


def test_doesnt_raise_error_if_all_viz_and_collect_exprs_are_aggregations():
    pgs = sgl_to_pgs("""
        visualize
            count(*) as x,
            avg(mpg) as y
        from cars
        collect by
            count(*)
        using lines
    """)
    layer = pgs["layers"][0]

    valid_groupings(layer)


def test_raises_error_if_group_by_omitted_and_not_all_viz_exprs_are_aggs():
    pgs = sgl_to_pgs("""
        visualize
            bin(mpg) as x,
            count(*) as y
        from cars
        collect by
            count(*)
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(SglError, match=re.escape(NO_GROUP_BY_MSG)):
        valid_groupings(layer)


def test_raises_error_if_group_by_omitted_and_not_all_collect_exprs_are_aggs():
    pgs = sgl_to_pgs("""
        visualize
            count(*) as x,
            count(*) as y
        from cars
        collect by
            bin(mpg),
            count(*)
        using lines
    """)
    layer = pgs["layers"][0]

    with pytest.raises(SglError, match=re.escape(NO_GROUP_BY_MSG)):
        valid_groupings(layer)
