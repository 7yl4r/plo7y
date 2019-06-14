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

from plo7y._internal.get_dataframe import get_dataframe


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
    savefig=None,
    title=None,
    ylabel=None,
    figsize=(12, 8),
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
    dta = get_dataframe(dta)
    # watch out for mutually-exclusive params
    assert sum([
        y_key is None,
        y_key_list is None
    ]) == 1

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

    if y_group_by_key is not None:
        dta.set_index(x_key, inplace=True)
        dta.groupby(y_group_by_key)[y_key].plot(x=x_key, y=y_key, legend=True)
    elif y_highlight_key is None:
        if y_key_list is not None:
            assert len(y_key_list) > 0
            _ts_compare_keylist(dta, x_key, y_key_list, figsize)
        elif y_key is not None:
            dta.plot(x=x_key, y=y_key)
        else:  # both None
            dta.plot(x=x_key, legend=legend)
    else:
        _ts_compare_highlight(
            dta, x_key, y_highlight_key, figsize, legend
        )

    if title is not None:
        plt.title(title)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if savefig is not None:
        plt.savefig(savefig, bbox_inches='tight')
    else:
        plt.show()


def _ts_compare_keylist(dta, x_key, y_key_list, figsize):
    """Compare several timeseries"""
    dta.plot(x=x_key, y=y_key_list[0])
    dta[y_key_list].plot(
        figsize=figsize
    )


def _ts_compare_highlight(
    dta, x_key, y_highlight_key, figsize, legend
):
    """How does the highlighted series differ from the others?"""
    axis = dta.plot(
        x=x_key, legend=legend, figsize=figsize,
        colormap='Pastel2',
        style=[':']*len(dta)
    )
    dta.plot(
        x=x_key, y=y_highlight_key, legend=legend, figsize=figsize,
        colormap='hsv',
        style=['-']*len(dta),
        ax=axis
    )
