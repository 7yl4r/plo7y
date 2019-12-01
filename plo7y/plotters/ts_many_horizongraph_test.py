from unittest import TestCase
import pandas as pd
import sys

from plo7y._tests import get_test_output_path
# TODO: use generated files instead of these:
from plo7y.get_test_data import get_test_data


class Test_prep_data(TestCase):
    def test_prep_dataframe_to_lists(self):
        from plo7y.plotters.ts_many_horizongraph import prep_data
        X = [1, 2, 3]
        Ya = [1, 4, 9]
        Yb = [3, 2, 1]
        LABELS = ['y1', 'y2']
        df = pd.DataFrame({
            "x": X,
            "y1": Ya,
            "y2": Yb
        })
        x, y, labels = prep_data(df, 'x', LABELS)
        self.assertEqual(x, X)
        self.assertEqual(y, [Ya, Yb])
        self.assertEqual(labels, LABELS)


class Test_horizongraph(TestCase):
    def test_many_horizongraph_on_lists(self):
        from plo7y.plotters.ts_many_horizongraph import _plot

        _plot(
            [1, 2, 3], [[11, 22, 33], [4, 3, 2]], [1, 2],
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )

    def test_many_horizongraph_on_dataframes(self):
        from plo7y.plotters.ts_many_horizongraph import plot
        x = get_test_data("./test_data/generated/linspace_x.csv")
        y1 = get_test_data("./test_data/generated/sine_1.csv")
        y2 = get_test_data("./test_data/generated/sine_2.csv")
        df = pd.concat([x, y1, y2], axis=1)
        print(df)
        plot(
            df, 'linspace_x', ['sine_1', 'sine_2'],
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
