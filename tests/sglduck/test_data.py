"""Tests for the bundled example datasets."""

import duckdb
import polars as pl

from sglduck import data, db_get_plot


def test_cars_shape_and_columns():
    cars = data.cars()
    assert isinstance(cars, pl.DataFrame)
    assert cars.shape == (406, 5)
    assert cars.columns == [
        "car_id",
        "horsepower",
        "miles_per_gallon",
        "origin",
        "year",
    ]


def test_trees_shape_and_columns():
    trees = data.trees()
    assert isinstance(trees, pl.DataFrame)
    assert trees.shape == (35, 3)
    assert trees.columns == ["tree_id", "age", "circumference"]


def test_each_call_returns_an_independent_frame():
    # loading is not a shared mutable singleton
    assert data.cars() is not data.cars()


def test_numeric_columns_are_numeric():
    # the "NA" missing-value markers must not make numeric columns strings, or
    # bin()/log() reject them (this broke the docs build).
    cars = data.cars()
    for col in ["car_id", "horsepower", "miles_per_gallon", "year"]:
        assert cars[col].dtype.is_numeric(), f"cars.{col} is {cars[col].dtype}"
    trees = data.trees()
    for col in ["age", "circumference"]:
        assert trees[col].dtype.is_numeric(), f"trees.{col} is {trees[col].dtype}"


def test_cars_renders_through_db_get_plot():
    con = duckdb.connect()
    con.register("cars", data.cars())
    svg = db_get_plot(
        con,
        "visualize horsepower as x, miles_per_gallon as y from cars using points",
    ).to_svg()
    assert "<svg" in svg
