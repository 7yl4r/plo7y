"""
NOTE: many of these tests only test that the plotting methods
    are able to finish without throwing an exception.
    TODO: Should we be checking the output figures somehow?
"""

from unittest import TestCase


class Test_ts_correlate(TestCase):
    def test_ts_correlation_basic(self):
        """Basic TS correlation report."""
        common_path = "plo7y/reporters/cross_correlation/cross_correllate_two"
        # from subprocess import run
        # run([
        #     "eggsmark", "knit",
        #     "./" + common_path + ".Rmd",
        #     "./examples/test_outputs/" + common_path + ".html"
        # ])
        from eggsmark.xmd_knit import knit
        knit(
            "./" + common_path + ".Rmd",
            "./examples/test_outputs/" + common_path + ".html"
        )
