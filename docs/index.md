# sglduck

**sglduck** implements the [SGL graphics language](https://arxiv.org/abs/2505.14690)
for Python. SGL is a grammar-of-graphics language designed to look and feel like
SQL. sglduck targets [DuckDB](https://duckdb.org) as its database and
[Lets-Plot](https://lets-plot.org) as its rendering backend.

## Installation

```sh
pip install sglduck
```

## Usage

[`db_get_plot`](reference.md) is the primary interface: it takes a DuckDB
connection and a SGL statement and returns the corresponding plot. The package
bundles a few example datasets (`sglduck.data`) to plot against.

```python exec="1" html="1" source="above"
import duckdb
import sglduck

con = duckdb.connect()
con.register("cars", sglduck.data.cars())

plot = sglduck.db_get_plot(
    con,
    """
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
    """,
)

# In a script, use plot.show() (opens a browser) or plot.save("plot.svg");
# in a Jupyter notebook the plot displays inline. This page embeds its SVG:
print(plot.to_svg())
```

## Next steps

- [Get started](get-started.md) — a tour of the SGL language and `db_get_plot`.
- [Example gallery](gallery.md) — a collection of plots generated with sglduck.
- [Reference](reference.md) — the public Python API.
- [SGL paper](https://arxiv.org/abs/2505.14690) — the language in depth, including
  its underlying grammar of graphics.
