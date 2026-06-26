"""Bundled example datasets.

``cars`` and ``trees`` mirror the datasets shipped with rsgl. They are loaded as
polars DataFrames for use with the SGL examples in the docs and tutorials, e.g.::

    import duckdb
    import sglduck

    con = duckdb.connect()
    con.register("cars", sglduck.data.cars())
"""

from __future__ import annotations

from importlib import resources

import polars as pl


def _load(filename: str) -> pl.DataFrame:
    source = resources.files(__package__) / filename
    with resources.as_file(source) as path:
        # "NA" marks missing values; scanning the whole (small) file means a
        # column with late floats or nulls still infers a numeric type — without
        # this, the "NA" strings make polars read numeric columns as strings.
        return pl.read_csv(path, null_values="NA", infer_schema_length=None)


def cars() -> pl.DataFrame:
    """The ``cars`` dataset: 406 cars by horsepower, miles per gallon, and origin.

    Columns: ``car_id``, ``horsepower``, ``miles_per_gallon``, ``origin``,
    ``year``. Derived from the vega-datasets ``cars.json`` — the kept fields
    ``Horsepower``, ``Miles_per_Gallon``, and ``Origin`` (renamed), ``year`` from
    the original ``Year`` date, and ``car_id`` a row id.
    """
    return _load("cars.csv")


def trees() -> pl.DataFrame:
    """The ``trees`` dataset: the growth of five orange trees over time.

    Columns: ``tree_id``, ``age`` (days since 1968-12-31), ``circumference``
    (mm). Derived from R's ``datasets::Orange``, with its ``Tree`` column renamed
    to ``tree_id``.
    """
    return _load("trees.csv")
