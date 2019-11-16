from unittest import TestCase
import matplotlib.pyplot as plt
import sys

from plo7y._tests import get_test_output_path


def get_sample_data():
    print("creating example covariance data.")
    import numpy as np
    import pandas as pd
    x_0 = -10
    x_f = 10
    dx = 200
    x = np.linspace(x_0, x_f, dx)
    y1 = np.sin(x+0) + np.random.normal(-0.1, 0.1, dx)
    y2 = np.sin(x-1) + np.random.normal(-0.1, 0.1, dx)
    # TODO: output this plot somewhere...
    plt.plot(x, y1)
    plt.plot(x, y2)
    # plt.show()
    plt.savefig(get_test_output_path(__file__, "sample_data"))
    plt.clf()
    dta = pd.DataFrame(y1)  # [x, y1, y2]  # TODO dataframe?
    exog = pd.DataFrame(y2)
    return dta, exog


class Test_ccf(TestCase):
    def tearDown(self):
        plt.clf()

    def test_ccf_plot_on_sample_data(self):
        from plo7y.plotters.ccf import plotCCF

        dta, exog = get_sample_data()
        plotCCF(
            dta, exog, saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )


class Test_cross_correlation(TestCase):
    def test_cross_correlation_on_sample_data(self):
        from plo7y.plotters.cross_correlation import plot

        dta, exog = get_sample_data()
        plot(
            # dta, exog,
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
