from unittest import TestCase
import matplotlib.pyplot as plt
import sys

from plo7y._tests import get_test_output_path
# TODO: use generated files instead of these:
from plo7y.generate_test_data import _get_testdata_noisy_sines
from plo7y.generate_test_data import _get_testdata_out_of_phase_sines


class Test_ccf(TestCase):
    def tearDown(self):
        plt.clf()

    def test_ccf_plot_on_phased_sines(self):
        from plo7y.plotters.ccf import plotCCF

        x, y1, y2 = _get_testdata_out_of_phase_sines()
        plotCCF(
            y1, y2, saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )


class Test_cross_correlation(TestCase):
    def test_cross_correlation_on_noisy_sines(self):
        from plo7y.plotters.cross_correlation import plot

        x, y1, y2 = _get_testdata_noisy_sines()
        plot(
            x.squeeze().to_numpy(),
            y1.squeeze().to_numpy(),
            y2.squeeze().to_numpy(),
            # dta, exog,
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )

    def test_cross_correlation_on_phased_sines(self):
        from plo7y.plotters.cross_correlation import plot

        x, y1, y2 = _get_testdata_out_of_phase_sines()
        plot(
            x.squeeze().to_numpy(),
            y1.squeeze().to_numpy(),
            y2.squeeze().to_numpy(),
            # dta, exog,
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
