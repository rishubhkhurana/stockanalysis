import numpy as np
import pandas as pd


def data_padding(data: pd.DataFrame, interval: int=60) -> pd.DataFrame:
    '''
    Function to pad the time series with different methods.
    :param data: pandas DataFrame containing values and indexed by some time stamp or date
    :param interval: time spacing for subsequent rows.
    :return: padded dataframe
    '''
    # forward filling
    data = data.reindex(range(data.index.min(), data.index.max()+60, 60), method='pad')
    #ToDo: Add other padding methods like linear interpolation etc.
    return data

def create_volume_bars(data: pd.DataFrame) -> pd.DataFrame:
    #ToDo: add code to create adaptive volume bars as per data at hand
    pass

def create_dollar_bars(data: pd.DataFrame) -> pd.DataFrame:
    #ToDo: add code to create adaptive dollar bars as per data at hand
    pass