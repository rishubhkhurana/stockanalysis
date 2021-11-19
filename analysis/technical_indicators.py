import numpy as np
import pandas as pd
from typing import List
import ta
import pandas_ta


def add_moving_average(data: pd.DataFrame,
                       window: int = 21,
                       api: str = 'pandas',
                      column: str='Close'):
    '''
    :param data:
    :param window:
    :param api:
    :param column:
    :return:
    '''
    assert column in data.columns, "Column not present in dataframe"
    if api=='pandas':
        data[column + '_ema' + str(window)] = data[column].ewm(span=window, min_periods=window)
        data[column + '_sma' + str(window)] = data[column].rolling(window=window).mean()
    elif api=='pandas_ta':
        data[column + '_ema' + str(window)] = pandas_ta.ema(data[column], length=window)
        data[column + '_sma' + str(window)] = pandas_ta.sma(data[column], length=window)
    elif api=='ta':
        ema = ta.trend.EMAIndicator(data[column], window=window)
        data[column + '_ema' + str(window)] = ema.ema_indicator()
        sma = ta.trend.SMAIndicator(data[column], window=window)
        data[column + '_sma' + str(window)] = sma.sma_indicator()

def add_macd(data: pd.DataFrame,
             window_slow: int = 26,
             window_fast: int = 12,
             window_sign: int = 9,
             api: str = 'pandas',
             column: str='Close'):
    assert column in data.columns, "Column not present in dataframe"
    if api=='pandas':
        fast_ema = data[column].ewm(span=window_fast, min_periods=window_fast)
        slow_ema = data[column].ewm(span=window_slow, min_periods=window_slow)
        MACD = pd.Series(fast_ema - slow_ema, name = f'MACD_{window_fast}_{window_slow}')
        MACDSign = MACD.ewm(span=window_sign, min_periods=window_sign)
        MACDDiff = MACD-MACDSign
        data[f'MACDDiff_{window_fast}_{window_slow}_{window_sign}'] = MACDDiff
        data[f'MACDSign_{window_fast}_{window_slow}_{window_sign}'] = MACDSign
        data[f'MACD_{window_fast}_{window_slow}'] = MACD
    elif api=='pandas_ta':
        temp = pandas_ta.macd(data[column], fast=window_fast, slow=window_slow, signal=window_sign)
        data[f'MACDDiff_{window_fast}_{window_slow}_{window_sign}'] = temp['MACD_12_26_9']
        data[f'MACDSign_{window_fast}_{window_slow}_{window_sign}'] = temp['MACDs_12_26_9']
        data[f'MACD_{window_fast}_{window_slow}'] = temp['MACDh_12_26_9']
    elif api=='ta':
        macd = ta.trend.MACD(data[column],
                             window_slow=window_slow,
                             window_fast=window_fast,
                             window_sign=window_sign)
        data[f'MACDDiff_{window_fast}_{window_slow}_{window_sign}'] = macd.macd_diff()
        data[f'MACDSign_{window_fast}_{window_slow}_{window_sign}'] = macd.macd_signal()
        data[f'MACD_{window_fast}_{window_slow}'] = macd.macd()