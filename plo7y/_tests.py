"""
These are helper methods for implementing tests.
"""

import os

TEST_DATA_DIR = "./test_data"


def ensure_path_exists(fpath):
    # print("\n\ncreating '{}'\n\n".format(fpath))
    os.makedirs(fpath, exist_ok=True)


def get_test_output_path(file_object, test_output_fname):
    THIS_TEST_SUB_PATH = file_object.split("/plo7y/")[1].split('_test.py')[0]
    TEST_OUTPUT_DIR = "./examples/test_outputs/{}".format(THIS_TEST_SUB_PATH)
    ensure_path_exists(TEST_OUTPUT_DIR)
    return "{}/{}".format(
        TEST_OUTPUT_DIR, test_output_fname
    )
