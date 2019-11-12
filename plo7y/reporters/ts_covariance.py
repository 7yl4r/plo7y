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
from plo7y.plotters.ccf import plotCCF


def report(*args, **kwargs):
    plotCCF(*args, **kwargs)
