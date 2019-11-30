from unittest import TestCase
import pandas as pd

from plo7y._tests import get_test_output_path
# TODO: use generated files instead of these:
from plo7y.generate_test_data import _get_testdata_noisy_sines


class Test_ccf_scipy(TestCase):
    def test_ccf_scipy_on_noisy_binary(self):
        from plo7y.plotters.arimax import plot
        data = pd.read_csv(
            "https://vincentarelbundock.github.io/Rdatasets/csv/MASS/drivers.csv"
        )
        data.index = data['time']
        data.loc[(data['time'] >= 1983.05), 'seat_belt'] = 1
        data.loc[(data['time'] < 1983.05), 'seat_belt'] = 0
        data.loc[(data['time'] >= 1974.00), 'oil_crisis'] = 1
        data.loc[(data['time'] < 1974.00), 'oil_crisis'] = 0
        plot(
            data, "value", ['oil_crisis']
        )
