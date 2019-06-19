"""Compare several pre-grouped timeseries using dataframe"""


def ts_compare_groupby(
    dta, x_key, y_key, figsize
):
    dta.plot(
        x=x_key, y=y_key, legend=True, figsize=figsize,
        kind='line',
    )
