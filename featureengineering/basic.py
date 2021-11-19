import numpy as np
import pandas as pd
from typing import List
import ta
import pandas_ta

def add_return_features(data: pd.DataFrame, 
                        column: str = 'Close', 
                        historicaltimebars: List = [1, 5, 15, 30, 60, 240],
                       ):
    '''
    Function that adds historical return features to the specified column
    :param data: dataframe containing the stock/asset data with different columns. dtype: pd.DataFrame
    :param column: name of column for which return features need to be added. dtype: str. Example: 'close'
    :param historicaltimebars: list of time intervals for which the historical return needs to be added. dtype: List
    :return: None

    '''
    for timebar in historicaltimebars:
        data[f'log_return_{column.lower()}_{timebar}'] = np.log(data[column]).diff(timebar)

def non_overlapping_window_features(data: pd.DataFrame,
                                    column: str,
                                    n_bars: int = 10,
                                    timeinterval: int = 15,
                                    agg: str = 'mean'):
    '''
    Function that computes historical features with non overlapping rolling windows.
    :param data:
    :param column:
    :param n_bars:
    :param timeinterval:
    :param agg:
    :return:
    '''
    # dictionary containing different aggregations supported
    funcs = {'mean':np.mean, 'std': np.std, 'sum':np.sum}
    # total span on which the statistic needs to be computed and aggregated
    span = n_bars*timeinterval
    # extract function
    f = funcs[agg]
    # extract the
    data[column+'_{agg}_{n_bars}'] = data[column].rolling(window=n_bars*timeinterval).agg(lambda x:
                                                                         f(x.iloc[list(range(0, n_bars*timeinterval,
                                                                                             timeinterval))]))

