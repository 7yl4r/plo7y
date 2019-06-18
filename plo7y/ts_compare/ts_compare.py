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
import seaborn

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
    dta = get_dataframe(dta)

    # watch out for mutually-exclusive params
    assert sum([
        y_key is None,
        y_key_list is None
    ]) == 1

    # error on unhandled params
    if dpi != 100:
        raise NotImplementedError("non-default dpi values NYI")

    # automatically pick best plotting method if needed
    if method is None:
        if y_group_by_key is not None:
            assert y_key is not None
            dta = dta.groupby([x_key, y_group_by_key]).agg({
                y_group_by_key: 'first',
                x_key: 'first',
                y_key: sum,
            })
            # dta.set_index(
            #     x_key, inplace=True, drop=False,
            #     # verify_integrity=True
            # )
            # aggregate across new index
            # dta = dta.groupby(level=0).agg(sum)
            grouped_dta = dta.groupby(y_group_by_key)[y_key]
            # === check for many overlapping points:
            # x-axis data-points-per-inch (dppi)
            x_dppi = grouped_dta.count().max() / figsize[0]

            # TODO: also check for many non-unique y-values at few x-values
            #    eg daily values binned to month.
            #    For these we can use a violin plot.

            if x_dppi > dpi/3:  # too dense
                if len(grouped_dta) == 2:
                    method = 'split-violin'
                else:
                    print(
                        "WARN: plotting method to handle too many x-values"
                        " not yet implemented; this plot might be ugly."
                    )
                    method = 'group-by-ed'
            else:
                method = 'group-by-ed'
        elif y_highlight_key is None:
            if y_key_list is not None:
                assert len(y_key_list) > 0
                method = 'key-list'
            elif y_key is not None:
                method = 'single-key'
                dta.plot(x=x_key, y=y_key)
            else:  # both None
                method = 'all-y'
                dta.plot(x=x_key, legend=legend)
        else:
            method = 'highlight'
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
        grouped_dta.plot(
            x=x_key, y=y_key, legend=True, figsize=figsize,
            kind='line',
        )
    elif method == 'key-list':
        _ts_compare_keylist(dta, x_key, y_key_list, figsize)
    elif method == 'single-key':
        dta.plot(x=x_key, y=y_key)
    elif method == 'all-y':  # both None
        dta.plot(x=x_key, legend=legend)
    elif method == 'highlight':
        _ts_compare_highlight(
            dta, x_key, y_highlight_key, figsize, legend
        )
    elif method == 'split-violin':
        dta.index = pandas.to_datetime(dta[x_key])
        # === downsample until we find a reasonable number of violins
        #    since I wasn't sure how to calculate the frequency of the
        #    existing dataset this brute-forces by starting at a huge
        #    resampling period & moving down until we get a good number
        #    of violins.
        PERIODS = [  # typical data frequency periods sorted descending
            '1200m', '120m', '60m', '24m', '12m', '6m',
            '120d', '90d', '30d', '14d', '7d', '1d',
        ]
        # ideal number of violins should be > LEN_MIN && < LEN_MAX
        LEN_MIN = 5
        LEN_MAX = 9
        assert len(dta) > LEN_MAX
        resample = []
        period_n = 0
        while len(resample) < LEN_MIN:
            new_period = PERIODS[period_n]
            print('resampling to frequency 1/{}...'.format(new_period))
            resample = dta.resample(new_period)
            # indexError here means we need to add smaller periods
            #     at the end of the list
            period_n += 1
        if len(resample) > LEN_MAX:
            raise AssertionError(
                "Oops, we went too far; "
                " more periods are needed between the last two."
            )
        else:
            print("success. Resampled into {} bins.".format(len(resample)))

        resample = resample.sum()[y_key]
        dta['x_resampled'] = [
            resample.index[resample.index.get_loc(
                pandas.to_datetime(v), method='nearest'
            )]
            for v in dta[x_key]
        ]

        # choose inner vizualization
        if len(dta) < figsize[0]*200 and len(dta) < 10000:
            inner_viz = "stick"
        else:
            inner_viz = "box"

        # choose amount of smoothing
        if len(dta) > 10000:
            bandwidth = 0.1
        elif len(dta) > 1000:
            bandwidth = 0.3
        else:
            bandwidth = None

        # do plot
        axes = seaborn.violinplot(
            x='x_resampled', y=y_key, hue=y_group_by_key, data=dta,
            scale="count",
            inner=inner_viz, bw=bandwidth,
            split=True, cut=0
        )
        axes.set_xticks([])
        axes.set_xlabel('{} / {}'.format(dta[x_key][0], dta[x_key][-1]))
    else:
        raise ValueError('unknown plotting method "{}"'.format(method))

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
