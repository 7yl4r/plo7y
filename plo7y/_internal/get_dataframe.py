import pandas as pd


def get_dataframe(data_thing):
    """
    Takes an arbitrary object and converts it into a standardized object
    all methods can use.
    """
    # dataframe passthrough
    if type(data_thing) == pd.core.frame.DataFrame:
        return data_thing
    # csv file path
    elif data_thing.strip().endswith(".csv"):
        data = pd.read_csv(data_thing)
        # drop any worthless columns
        data.dropna(axis='columns', how='all', inplace=True)
        return data
