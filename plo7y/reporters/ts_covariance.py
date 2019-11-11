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
from plo7y.plotters.ccf import plotCCF


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
    plotCCF(dta, exog, None)
