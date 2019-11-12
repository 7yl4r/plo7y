# plo7y
`plo7y` is a collection of wrappers around python data visualizations organized by the goal, objective, or question relevant to the visualization.

----------------------------------------------------------------------------

This concept is meant to expand on [this blog post](http://7ych.blogspot.com/2017/06/best-data-visualizations-in-python.html).

----------------------------------------------------------------------------

## Thoughts:

Tests run on example data from packages or generated using a specific random seed.
Test outputs write to `examples/test_outputs/`.
Tests exist alongside code and are collected & run via pytest.

### rules/assumptions
* all data inputs should be .csv files (with headers?)?

### Definitions
* *data*: data that can be passed into one of the "method types" below. Can be:
    - pandas DataFrame
    - csv file object
    - str path to a file
* *ts*: timeseries
* **plot type**:
    - string used as a "key" to identify a plot. eg "bar", "pie", "scatter".
* **plot metadata**
    - dict containing keys/tags and values to characterize a **plot type** and/or a **plotter** implementation.
    - **plotters** are described by a structured set of metadata in a dict.
        Example:

        ```
        _plotter_metadata = {
            "data_type": "timeseries",
            "n_data_min": 2,
            "n_data_max": 12,
            "tags": ["line", "color", "scatter"],
        }
        ```
    - This metadata can be used by recommender methods to choose the ideal plotting method.
#### Abstract "method types"
* **recommender**:
    - computes statistics & returns string representing suggested plot type
    - _input_ : data & **plot metadata** of all plots to consider
    - _output_: identification of **plot type** and **plotter** implementation to use
* **plotter**:
    - implements a **plot type**
    - characterized by **plot metadata** dict
    - _input_ : data & plot kwargs
    - _output_: .html, image, or other plot representation
        * (?) all viz outputs should be .hmtl (?)
* **tester**: performs specific statistical test for **recommenders**
    - _input_ : data & statistical kwargs
    - _output_: statistical test results as... (?)dict(?)
* **reporter**: verbose versions of **recommender** which output reports supporting the conclusion
    - _input_ : data & kwargs
    - _output_: report as .html, .Rmd, other?

### directory structure
```
/plo7y/
    /plotters/  # plot implementations
        /{plot-type-key}.py
    /recommenders/  # plotting method suggesters
        /{vizualization-goal}.py
    /testers/  # specific statistical tests
        /{data_type}Analyzer.py
        /_commmon/{generalizable_test_name}.py
    /reporters/  # reports (TODO: should be Rmd or ipynb?)
        /{report-goal}.py
```


### report usage
Reports can be written as [parameterized .Rmd documents](https://bookdown.org/yihui/rmarkdown/parameterized-reports.html), interactive python scripts, or
(assuming these exist) parameterized jupyter notebooks.

#### jupyter reports
No Jupyter notebook reports exist yet, but they are theoretically possible.

#### py script reports
Interactive python scripts should be called from a python console or executed from the command line as usual.

#### R markdown reports
Parameterized `.Rmd` reports can be included as "child" chunks within a parent `.Rmd`.
Because the path of the child may not be easily known, it is recommended to instead use the `rmarkdown::render` function directly within an R console, script, or a parent `.Rmd` file's chunk.
An example of this usage is below:

```r
# find the path of plo7y module:
plo7y_path = system(
    "python -c 'import plo7y; print(plo7y.__file__.split(\"/__init__.py\")[0])'",
    intern=TRUE
)
# append the name of the report .Rmd
report_path = paste(plo7y_path, "/reporters/ts_compare.Rmd", sep="")
# render the report here
rmarkdown::render(report_path, params = list(
  year = 2017,
  region = "Asia",
  printcode = FALSE,
  file = "file2.csv"
))
```
