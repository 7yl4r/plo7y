"""Compare several pre-grouped timeseries using dataframe"""


def ts_compare_groupby(
    dta, x_key, y_key, y_group_by_key, figsize
):
    grouped_dta = dta.groupby([y_group_by_key]).agg({
        y_group_by_key: 'first',
        x_key: 'first',
        y_key: sum,
    })[y_key]
    grouped_dta.plot(
        x=x_key, y=y_key, legend=True, figsize=figsize,
        kind='line',
    )
