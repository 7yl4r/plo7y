"""
Compare a set of N timeseries.

Examples:
---------
* stock prices
* portfolio values
* temperatures in two locations

TODO: use horizonplots for large N?
TODO: use image for huge N?

"""
import pandas

from plo7y._internal.get_dataframe import get_dataframe
from plo7y.testers.TSAnalyzer.TSAnalyzer import TSAnalyzer


def recommend(
    dta,
    y_key,
    x_key,
    y_key_list,
    dpi,
    y_group_by_key,
    figsize,
    y_highlight_key
):
    """
    Parameters
    ----------
    dta : pandas.DataFrame
        dataframe containing all columns
    x_key : str
        x-axis column name
    y_key : str
        y-axis column name
    y_key_list : str[]
        y-axis column names (for multiple y_key)
    y_group_by_key : str
        a single column with catagorical values used which
        will be grouped to add multiple series to the y-axis
    savefig : str
        filepath to save output, else show
    """
    # pre-checks & preproc
    dta = get_dataframe(dta)
    if y_key is not None:
        dta[y_key] = pandas.to_numeric(dta[y_key])

    assert x_key is not None
    assert dta[x_key].nunique() > 1

    # watch out for mutually-exclusive params
    if sum([
        y_key is None,
        y_key_list is None
    ]) != 1:
        raise ValueError("y_key or y_key_list must be provided")

    # error on unhandled params
    if dpi != 100:
        raise NotImplementedError("non-default dpi values NYI")

    ts_analyzer = TSAnalyzer(dta)
    # automatically pick best plotting method if needed
    if (
        y_group_by_key is not None and
        ts_analyzer.is_x_too_dense(
            x_key, y_key, y_group_by_key, figsize, dpi
        ) and
        len(ts_analyzer.grouped_dta(y_group_by_key, x_key, y_key)) == 2
    ):
        assert y_key is not None
        # TODO: also check for many non-unique y-values at few x-values
        #    ie: ordered catagorical data.
        #    eg: daily values binned to month.
        #    For these we can use
        #        if many values: violin plot
        #        else not so many seaborn catplot

        method = 'split-violin'
    elif (
        y_group_by_key is not None and
        ts_analyzer.is_x_too_dense(x_key, y_key, y_group_by_key, figsize, dpi)
    ):
        print(
            "WARN: plotting method to handle too many x-values"
            " not yet implemented; this plot might be ugly."
        )
        method = 'group-by-ed'
    elif (
            y_group_by_key is not None
    ):
        method = 'group-by-ed'
    elif y_highlight_key is not None:
        method = 'highlight'
    elif y_key_list is not None:
        assert len(y_key_list) > 0
        method = 'key-list'
    elif y_key is not None:
        method = 'single-key'
    else:
        method = 'all-y'

    assert method is not None
    return method
