from unittest import TestCase
import matplotlib.pyplot as plt
import sys

from plo7y.plotters.ccf import plotCCF
from plo7y._tests import get_test_output_path


class Test_tsne(TestCase):
    def test_tsne_sample_data(self):
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

        dta = pd.DataFrame(y1)  # [x, y1, y2]  # TODO dataframe?
        exog = pd.DataFrame(y2)
        plotCCF(
            dta, exog, saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
