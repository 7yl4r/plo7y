import pandas as pd
import os


def load_data(fpath):
    return pd.read_csv(
        fpath, index_col=0, names=[os.path.basename(fpath).split('.')[0]]
    )


def get_test_data(fpath):
    try:
        data = load_data(fpath)
    except FileNotFoundError:
        from plo7y.generate_test_data import generate_test_data
        generate_test_data()
        try:
            data = load_data(fpath)
        except FileNotFoundError:
            raise AssertionError("unable to get test_data/generated/")
    return data
