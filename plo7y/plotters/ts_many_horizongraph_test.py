from unittest import TestCase
import matplotlib.pyplot as plt
import sys

from plo7y._tests import get_test_output_path
# TODO: use generated files instead of these:
from plo7y.generate_test_data import _get_testdata_out_of_phase_sines


class Test_horizongraph(TestCase):
    def test_many_horizongraph(self):
        from plo7y.plotters.ts_many_horizongraph import plot

        plot(
            [1,2,3], [[11,22,33],[4,3,2]], [1, 2],
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
