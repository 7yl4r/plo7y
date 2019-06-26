# plo7y
`plo7y` is a collection of wrappers around python data visualizations organized by the goal, objective, or question relevant to the visualization.

----------------------------------------------------------------------------

This concept is meant to expand on [this blog post](http://7ych.blogspot.com/2017/06/best-data-visualizations-in-python.html).

----------------------------------------------------------------------------

## Thoughts:

### rules/assumptions
* all data inputs should be .csv files (with headers?)?
* all viz outputs should be .hmtl?

### Abstract method types
* **plot type**: string used as a "key" to identify a plot. eg "bar", "pie", "scatter".
* **recommender**: computes statistics & returns string representing suggested plot type
* **plotter**: implements a plot type
* **tester**: performs specific statistical test for **recommenders**
* **reporter**: verbose versions of **recommender** which output reports supporting the conclusion

### directory structure
```
/plo7y/
    /plotters/
        /bar_multiple_stacked
        /bar_multiple_horiz
        /scatter_single_series
    /recommenders/
        /ts_compare
        /ts_seasonality
```

### plotter metadata
**plotters** are described by a structured set of metadata in a dict.
Example:

```
_plotter_metadata = {
    "data_type": "timeseries",
    "n_data_min": 2,
    "n_data_max": 12,
    "tags": ["line", "color", "scatter"],
}
```

### definitions, terms, abbreviations
* ts: timeseries
