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

def add_range_features(data: pd.DataFrame,
                       range_columns: List = ['High', 'Low']):
    if not isinstance(range_columns, list):
        raise ValueError("range type should be a list of columns")
    if re.search(r'_', range_columns[0]):
        col_typ_first = range_columns[0].split('_')[-1][0]
    else:
        col_typ_first = range_columns[0][0]
    if re.search(r'_', range_columns[1]):
        col_typ_second = range_columns[1].split('_')[-1][0]
    else:
        col_typ_second = range_columns[1][0]
    col_typ = col_typ_first + col_typ_second
    data[f'delta_range_{col_typ}'] = data[range_columns[0]] - data[range_columns[1]]
    data[f'ratio_range_{col_typ}'] = data[range_columns[0]].divide(data[range_columns[1]])

def add_window_features(data: pd.DataFrame,
                        colname: str = '',
                        column: str = '',
                        window: int = 20,
                        agg: str = 'mean',
                        custom_func = None,
                        **kwargs):
    funcs = ['mean', 'std', 'max', 'min', 'sum', 'custom']
    if len(column)==0:
        raise ValueError("Column name cannot be empty")
    if agg not in funcs:
        raise ValueError(f"Aggregate functions not in {funcs}")
    if len(colname)==0:
        colname = column + f'_{window}' + f'_{agg}'
    if agg=='mean':
        data[colname] =  data[column].rolling(window=window, **kwargs).mean()
    elif agg=='std':
        data[colname] =  data[column].rolling(window=window, **kwargs).std()
    elif agg=='max':
        data[colname] =  data[column].rolling(window=window, **kwargs).max()
    elif agg=='min':
        data[colname] =  data[column].rolling(window=window, **kwargs).min()
    elif agg=='sum':
        data[colname] =  data[column].rolling(window=window, **kwargs).sum()
    else:
        data[colname] =  data[column].rolling(window=window, **kwargs).agg(custom_func)