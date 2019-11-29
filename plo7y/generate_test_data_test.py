"""
Tests the ability to generate test data.
Bonus: if you can make this test run first it will generate needed test data.
"""

from unittest import TestCase
from plo7y._tests import md5


class Test_generate_test_data(TestCase):
    def test_generate_binary_time_series(self):
        """Generate binary time series."""
        from plo7y.generate_test_data import generate_test_data
        generate_test_data()
        self.assertEqual(
            md5("./test_data/generated/timeseries_binary_signal.csv"),
            "1af2b7c32dea4219e0ac286514e7daa9"
        )
