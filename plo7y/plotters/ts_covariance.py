"""
Explore co-variance in two timeseries.
Will show markov chain prediction of one series for the other.
Will show one series as predictor of the other with time lag.
Will show series alternating as predictors of the other in time by comparing
cross-correlation function results.

Examples:
---------
* two stock prices
* temperatures in two nearby locations
* tide gauges on coast and up an estuary
"""
import matplotlib.pyplot as plt

from plo7y._internal.get_dataframe import get_dataframe
from plo7y.recommenders.ts_compare import recommend


def ts_compare(
    dta,
    figsize=(10, 7.5),  # width, height in inches (default 100 dpi)
    dpi=100,
    legend=True,
    savefig=None,
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
    if kwargs.get("method") is None:
        method = recommend(
            dta,
            dpi=dpi,
            figsize=figsize,
            legend=legend,
            **kwargs
        )

    # timeseries rows must be in order
    dta.sort_values(kwargs.get("x_key"), inplace=True)

    # === drop missing values:
    orig_len = len(dta)
    if kwargs.get("y_key_list") is not None:
        col_list = kwargs.get("y_key_list") + [kwargs.get("x_key")]
    elif kwargs.get("y_group_by_key") is not None:
        col_list = [
            kwargs.get("y_group_by_key"),
            kwargs.get("x_key"),
            kwargs.get("y_key")
        ]
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
    method(dta=dta)

    if kwargs.get("title") is not None:
        plt.title(kwargs.get("title"))
    if kwargs.get("ylabel") is not None:
        plt.ylabel(kwargs.get("ylabel"))

    if savefig is not None:
        plt.savefig(savefig, bbox_inches='tight')
        plt.clf()
    else:
        plt.show()

if __name__ == "__main__":
    print("creating example covariance data.")
    import numpy as np
    import pandas as pd
    x_0 = -10
    x_f = 10
    dx = 200
    x = np.linspace(x_0, x_f, dx)
    y1 = np.sin(x+0) + np.random.normal(-0.1, 0.1, dx)
    y2 = np.sin(x-1) + np.random.normal(-0.1, 0.1, dx)
    plt.plot(x, y1)
    plt.plot(x, y2)
    # plt.show()

    dta = pd.DataFrame(y1)  # [x, y1, y2]  # TODO dataframe?
    exog = pd.DataFrame(y2)
    from plo7y.plotters.ccf import plotCCF
    plotCCF(dta, exog, None)
