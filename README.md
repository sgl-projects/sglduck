# sglduck

sglduck implements the [SGL graphics
language](https://arxiv.org/pdf/2505.14690) for use within Python. SGL is a
graphics language that is designed to look and feel like SQL, and is
based on the grammar of graphics. sglduck targets [DuckDB](https://duckdb.org)
as its database and [Lets-Plot](https://lets-plot.org) as its graphics backend.

> **Status:** early development (pre-release). The API shown below is the
> intended public interface and is not yet fully implemented.

## Installation

Install the latest release from [PyPI](https://pypi.org/project/sglduck/):

``` sh
pip install sglduck
```

If you instead want the development version, install from GitHub with:

``` sh
pip install git+https://github.com/sgl-projects/sglduck
```

## Usage

`db_get_plot` is the primary interface to sglduck. It takes a DuckDB
connection and a SGL statement and returns the corresponding plot.

The following example demonstrates creating a connection to an in-memory
[DuckDB](https://duckdb.org) database, loading it with data, and then
generating a scatterplot from a SGL statement.

``` python
import duckdb
import sglduck

con = duckdb.connect()
con.execute("create table cars as select * from 'cars.csv'")

db_get_plot(con, """
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
""")
```
