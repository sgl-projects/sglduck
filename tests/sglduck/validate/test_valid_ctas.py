"""Tests for valid_ctas."""

import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.validate import valid_ctas

VALID_EXPRS = [
    pytest.param("hp", id="identity"),
    pytest.param("bin(mpg)", id="bin"),
    pytest.param("count(*)", id="count"),
]
INVALID_EXPRS = [
    pytest.param("*", id="identity"),
    pytest.param("bin(cut)", id="bin"),
    pytest.param("count(cut)", id="count"),
]


def assert_valid_ctas_passes(sgl, con):
    pgs = sgl_to_pgs(sgl)
    df = result_dfs(pgs, con)[0]
    layer = pgs["layers"][0]

    valid_ctas(layer, df)


def assert_valid_ctas_raises(sgl, con):
    pgs = sgl_to_pgs(sgl)
    df = result_dfs(pgs, con)[0]
    layer = pgs["layers"][0]

    with pytest.raises(SglError):
        valid_ctas(layer, df)


@pytest.mark.parametrize("expr", VALID_EXPRS)
def test_doesnt_raise_error_for_valid_ctas_in_aes_mapping(test_con, expr):
    assert_valid_ctas_passes(
        f"""
        visualize
            {expr} as x
        from cars
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize("expr", VALID_EXPRS)
def test_doesnt_raise_error_for_valid_ctas_in_group_by_clause(test_con, expr):
    assert_valid_ctas_passes(
        f"""
        visualize
            hp as x
        from cars
        group by
            {expr}
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize("expr", VALID_EXPRS)
def test_doesnt_raise_error_for_valid_ctas_in_collect_by_clause(test_con, expr):
    assert_valid_ctas_passes(
        f"""
        visualize
            hp as x
        from cars
        collect by
            {expr}
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize("expr", INVALID_EXPRS)
def test_raises_error_for_invalid_ctas_in_aes_mapping(test_con, expr):
    assert_valid_ctas_raises(
        f"""
        visualize
            {expr} as x
        from diamonds
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize("expr", INVALID_EXPRS)
def test_raises_error_for_invalid_ctas_in_group_by_clause(test_con, expr):
    assert_valid_ctas_raises(
        f"""
        visualize
            price as x
        from diamonds
        group by
            {expr}
        using points
        """,
        test_con,
    )


@pytest.mark.parametrize("expr", INVALID_EXPRS)
def test_raises_error_for_invalid_ctas_in_collect_by_clause(test_con, expr):
    assert_valid_ctas_raises(
        f"""
        visualize
            price as x
        from diamonds
        collect by
            {expr}
        using points
        """,
        test_con,
    )


def test_doesnt_raise_error_for_valid_ctas_across_multiple_clauses(test_con):
    pgs = sgl_to_pgs("""
        visualize
            bin(carat) as x,
            count(*) as y,
            cut as color
        from diamonds
        group by
            bin(carat),
            cut
        collect by
            cut
        using lines
    """)
    df = result_dfs(pgs, test_con)[0]
    layer = pgs["layers"][0]

    valid_ctas(layer, df)
