"""
Get detailed analysis of a timeseries.
"""
from functools import lru_cache


class TSAnalyzer():
    # TODO: trend & frequency analysis
    # TODO: normality of residuals
    # TODO: autocorrelation
    # pd.plotting.autocorrelation_plot(df[y_key])
    # TODO: is_stationary
    # TODO: differencing to make stationary
    # df[y_key].diff(periods=30).plot()

    # https://github.com/datascopeanalytics/traces

    def __init__(self, dataframe):
        self.df = dataframe

    @property
    @lru_cache()
    def is_evenly_spaced(self):
        """
        True if timedelta between each pair of points is the same.
        Assumes series is sorted & index is datetimes.
        """
        t_col = self.df.index
        expected_td = t_col[0] - t_col[1]
        for i in range(len(t_col)-1):  # for each pair of points
            if t_col[i] - t_col[i+1] != expected_td:
                return False
        else:
            return True
