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
import matplotlib.pyplot as plt
import pandas

from plo7y._internal.get_dataframe import get_dataframe
from plo7y.plotters.ts_line_compare_keylist import ts_compare_keylist
from plo7y.plotters.ts_line_compare_highlight import ts_compare_highlight
from plo7y.plotters.ts_line_compare_groupby import ts_compare_groupby
from plo7y.plotters.ts_two_violin_compare_downsample \
    import ts_downsample_compare_two


def x_too_dense(dta, x_key, y_key, y_group_by_key, figsize, dpi):
    x_dppi = len(dta.groupby(x_key)) / figsize[0]

    if x_dppi > dpi/3:  # too dense
        return True
    else:
        return False


def ts_compare(
    dta,
    *args,
    x_key=None,
    y_key=None,
    y_key_list=None,
    y_group_by_key=None,
    y_highlight_key=None,
    # TODO: some of these args are generalizable...
    #       how best to share them between functions?
    method=None,
    savefig=None,
    title=None,
    ylabel=None,
    figsize=(10, 7.5),  # width, height in inches (default 100 dpi)
    dpi=100,
    legend=True,
    **kwargs
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

    # automatically pick best plotting method if needed
    if method is None:
        if y_group_by_key is not None:
            assert y_key is not None
            grouped_dta = dta.groupby([y_group_by_key]).agg({
                y_group_by_key: 'first',
                x_key: 'first',
                y_key: sum,
            })[y_key]
            if (
                x_too_dense(
                    dta, x_key, y_key, y_group_by_key, figsize, dpi
                ) and
                len(grouped_dta) == 2
            ):
                # TODO: also check for many non-unique y-values at few x-values
                #    ie: ordered catagorical data.
                #    eg: daily values binned to month.
                #    For these we can use
                #        if many values: violin plot
                #        else not so many seaborn catplot

                    method = 'split-violin'
            elif x_too_dense(
                dta, x_key, y_key, y_group_by_key, figsize, dpi
            ):
                print(
                    "WARN: plotting method to handle too many x-values"
                    " not yet implemented; this plot might be ugly."
                )
                method = 'group-by-ed'
            else:
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

    # timeseries rows must be in order
    dta.sort_values(x_key, inplace=True)

    # === drop missing values:
    orig_len = len(dta)
    if y_key_list:
        col_list = y_key_list + [x_key]
    elif y_group_by_key:
        col_list = [y_group_by_key, x_key, y_key]
    else:
        raise ValueError(
            "Must pass multiple y-cols or give group-by col."
        )
    dta.dropna(subset=col_list, inplace=True)
    print("{} NA values-containing rows dropped; {} remaining.".format(
        orig_len - len(dta), len(dta)
    ))
    if len(dta) < 2:
        raise ValueError("Too few valid rows to create plot.")

    # do the plotting
    print('plotting w/ method "{}"'.format(method))
    if method == 'group-by-ed':
        ts_compare_groupby(grouped_dta, x_key, y_key, figsize)
    elif method == 'key-list':
        ts_compare_keylist(dta, x_key, y_key_list, figsize)
    elif method == 'single-key':
        dta.plot(x=x_key, y=y_key)
    elif method == 'all-y':  # both None
        dta.plot(x=x_key, legend=legend)
    elif method == 'highlight':
        ts_compare_highlight(
            dta, x_key, y_highlight_key, figsize, legend
        )
    elif method == 'split-violin':
        ts_downsample_compare_two(dta, x_key, y_key, y_group_by_key, figsize)
    else:
        raise ValueError('unknown plotting method "{}"'.format(method))

    if title is not None:
        plt.title(title)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if savefig is not None:
        plt.savefig(savefig, bbox_inches='tight')
        plt.clf()
    else:
        plt.show()
