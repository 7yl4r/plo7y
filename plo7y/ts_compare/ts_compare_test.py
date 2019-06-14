"""
"""

# std modules:
from unittest import TestCase

from plo7y.ts_compare.ts_compare import ts_compare


class Test_ts_compare(TestCase):
    # tests:
    #########################
    def test_obis_occurrence(self):
        """ test ts compare on obis occurence data """
        ts_compare(
            "test_data/obis.csv",
            x_key="year",
            y_key_list=["X", "aphiaID", "year"]
        )
