# Example gallery

A collection of plots generated with sglduck, organized by dataset. The examples
use an in-memory DuckDB database loaded with the bundled datasets, and the same
`render` helper as the [Get started](get-started.md) guide.

```python exec="1" source="above" session="gallery"
import duckdb
import sglduck

con = duckdb.connect()
con.register("cars", sglduck.data.cars())
con.register("trees", sglduck.data.trees())


def render(sgl):
    print(sglduck.db_get_plot(con, sgl).to_svg())
```

## Cars

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
""")
```

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using (
        points
        layer
        regression line
    )
    facet by
        origin
    scale by
        log(x),
        log(y)
""")
```

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        count(*) as theta,
        origin as color
    from cars
    group by
        origin
    using bars
    title
        theta as 'Number of Cars',
        color as 'Country of Origin'
""")
```

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        bin(miles_per_gallon) as x,
        count(*) as y
    from cars
    group by
        bin(miles_per_gallon)
    using bars
""")
```

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        origin as x,
        miles_per_gallon as y
    from cars
    using boxes
    scale by
        log(y)
""")
```

## Trees

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        age as x,
        circumference as y
    from trees
    collect by
        tree_id
    using lines
""")
```

```python exec="1" html="1" source="above" session="gallery"
render("""
    visualize
        age as theta,
        radius as r
    from (
        select
            *,
            circumference / (2 * pi()) as radius
        from trees
    )
    collect by
        tree_id
    using lines
""")
```
