# Get started

This guide introduces the SGL language and the sglduck package.

## Setup

The examples use an in-memory [DuckDB](https://duckdb.org) database loaded with
the bundled `cars` and `trees` datasets. `db_get_plot` returns an
[`SglPlot`](reference.md); for brevity this guide wraps it in a small `render`
helper that displays the plot (in your own code you would use `plot.show()`, or
display the plot in a Jupyter notebook).

```python exec="1" source="above" session="guide"
import duckdb
import sglduck

con = duckdb.connect()
con.register("cars", sglduck.data.cars())
con.register("trees", sglduck.data.trees())


def render(sgl):
    print(sglduck.db_get_plot(con, sgl).to_svg())
```

## The SGL language

### The from clause

The `from` keyword precedes a data source, often the name of a table. Here we
use the `cars` table.

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
""")
```

This resembles SQL's `from`, except that only a single data source is allowed.
If data from multiple sources or pre-processing is needed, a SQL subquery can be
provided:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from (
        select *
        from cars
        where origin = 'Japan'
    )
    using points
""")
```

### The using clause

The `using` keyword precedes the geometric object(s) that represent the data.
Following ggplot2 terminology, these are referred to as geoms. The examples above
represent data with point geoms.

### The visualize clause

The `visualize` keyword precedes the aesthetic-to-column mapping, which maps
perceivable traits of the geoms to data source columns. The prior examples
mapped the `x` and `y` positions of point geoms; aesthetics may also be
non-positional, such as `color`. `visualize` most closely resembles SQL's
`select`.

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y,
        origin as color
    from cars
    using points
""")
```

### Column-level transformations and aggregations

SGL supports column-level transformations and aggregations. Below, a binning
transformation is combined with a count aggregation to produce a histogram of
`miles_per_gallon`. As in SQL, aggregation groupings are specified in a
`group by` clause.

```python exec="1" html="1" source="above" session="guide"
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

SGL's column-level transformations and aggregations are performed *after*
scaling, which cannot easily be replicated in SQL. Below, binning and counting
are applied after log scaling, producing a log-scaled histogram:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        bin(miles_per_gallon) as x,
        count(*) as y
    from cars
    group by
        bin(miles_per_gallon)
    using bars
    scale by
        log(x)
""")
```

### The collect by clause

A geom is *individual* if it represents each record by a distinct object, and
*collective* if it represents multiple records by one object. Points and lines
are individual and collective, respectively — here the same data is shown with
each:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        year as x,
        avg(miles_per_gallon) as y
    from cars
    group by
        year
    using points
""")
```

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        year as x,
        avg(miles_per_gallon) as y
    from cars
    group by
        year
    using line
""")
```

For collective geoms, the records collected into each object are chosen
automatically by default. The `collect by` clause overrides this — it is like
`group by`, but defines collections to represent by one object rather than groups
to aggregate. Below, the default collection is not ideal, followed by an explicit
collection:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        age as x,
        circumference as y
    from trees
    using line
""")
```

```python exec="1" html="1" source="above" session="guide"
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

### Geom qualifiers

Geom qualifiers modify how geoms positionally represent data, written as keywords
before the geom name in the `using` clause. *Statistical* qualifiers apply a
statistical transformation, such as linear regression:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        age as x,
        circumference as y
    from trees
    using regression line
""")
```

*Collision* qualifiers adjust the positions of overlapping objects. Below, the
`jittered` qualifier adds a small amount of random variation so overlapping
points are discernible:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        origin as x,
        miles_per_gallon as y
    from cars
    using jittered points
""")
```

### The layer operator

A graphic may combine multiple layers of geoms with the `layer` operator. For
example, layering a regression line on a scatterplot:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points

    layer

    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using regression line
""")
```

When layers share a data source and aesthetic mapping, the `layer` operator can
be applied directly to geom expressions to reduce verbosity:

```python exec="1" html="1" source="above" session="guide"
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
""")
```

A graphic has a single scale for each aesthetic across all layers, so an
aesthetic must be mapped to a consistent type in every layer where it appears.

### The scale by clause

Each mapped aesthetic has a scale that determines how data values map to the
visual property. Scales are implicit by default but can be set in the `scale by`
clause. Here `log` scales override the default linear scaling on `x` and `y`:

```python exec="1" html="1" source="above" session="guide"
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
    scale by
        log(x), log(y)
""")
```

Scaling is performed prior to column-level transformations, aggregations, and
geom-qualifier adjustments — so the regression above is computed on the
log-scaled values. Scaling functions like `log` apply to aesthetic names rather
than column names, because they modify aesthetic scales rather than the data.

### Coordinate systems

The coordinate system is inferred from the positional aesthetics: `x` and `y`
imply Cartesian coordinates, while `theta` and `r` imply polar coordinates. In
the grammar of graphics, a pie chart is a stacked bar chart in polar coordinates
— and the bar geom is stacked by default. The same data, in Cartesian and polar
coordinates:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        count(*) as y,
        origin as color
    from cars
    group by
        origin
    using bars
""")
```

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        count(*) as theta,
        origin as color
    from cars
    group by
        origin
    using bars
""")
```

### The facet by clause

Faceting generates small multiples, each panel a partition of the source data by
the unique values of the `facet by` expressions. A single expression generates
horizontal panels by default, which an orientation keyword can change:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
    facet by
        origin
""")
```

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
    facet by
        origin vertically
""")
```

Two facet expressions place one horizontally and the other vertically:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from (
        select
            *,
            case
                when year < 1977 then '< 1977'
                else '>= 1977'
            end as 'era'
        from cars
    )
    using points
    facet by
        era,
        origin
""")
```

### The title clause

Aesthetic-scale titles are determined automatically from the mappings, but can be
overridden in the `title` clause:

```python exec="1" html="1" source="above" session="guide"
render("""
    visualize
        horsepower as x,
        miles_per_gallon as y
    from cars
    using points
    title
        x as 'Horsepower',
        y as 'Miles Per Gallon'
""")
```

## Next steps

- [Example gallery](gallery.md) — a collection of plots generated with sglduck.
- [Reference](reference.md) — the public Python API.
- [SGL paper](https://arxiv.org/abs/2505.14690) — the language in greater depth.
