"""
NOTE: many of these tests only test that the plotting methods
    are able to finish without throwing an exception.
    TODO: Should we be checking the output figures somehow?
"""
import sys
from unittest import TestCase

from plo7y.reporters.optimization.tsne import main
from plo7y._tests import get_test_output_path


class Test_tsne(TestCase):
    def test_tsne_sample_data(self):
        """Test tsne optimization on sample data"""
        from sklearn import datasets
        import pandas as pd
        location, value = datasets.make_circles(
            n_samples=1000, factor=.5, noise=.05
        )
        df = pd.DataFrame(
            columns=['var1', 'var2', 'var3', 'score']
        )
        df['var1'] = location[:, 0]
        df['var2'] = location[:, 1]
        df['var3'] = location[:, 1]  # TODO: other data?
        df['score'] = value

        # import pdb; pdb.set_trace()
        main(
            df,
            "var1", "var2", "var3",
            saveFigPath=get_test_output_path(
                __file__, sys._getframe().f_code.co_name
            )
        )
