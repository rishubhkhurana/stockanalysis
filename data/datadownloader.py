from .regimports import *
from .namemapping import *
from .api_keys import *

supported_frameworks = ['yahoo_fin', 'alphavantage', 'backtesting', 'investpy']

def get_daily_historical_data(ticker,
             country='United States',
             start_date=None,
             end_date=None,
             framework = 'yahoo_fin'):
    if framework not in supported_frameworks:
        raise ValueError("Only yahoo_fin and alphavantage supported")
    ticker = namemap.get(ticker, ticker)
    try:

        if framework == 'yahoo_fin':
            df = si.get_data(ticker, start_date=start_date,end_date=end_date)
        elif framework == 'backtesting':
            df = bt.get(ticker, start=start_date, end=end_date)
        elif framework == 'alphavantage':
            key = API['alphavantage']
            ts = TimeSeries(key, output_format='pandas')
            df, metadata = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            df = df.loc[::-1].loc[start_date:end_date]
        elif framework == 'investpy':
            df = ipy.get_stock_historical_data(stock=ticker,
                                               country=country,
                                               from_date=start_date,
                                               to_date=end_date)
    except:
        df = None
    return df

def get_daily_historical_fundamental_data(ticker,
             country='United States',
             start_date=None,
             end_date=None,
             framework = 'yahoo_fin'):
    if framework not in supported_frameworks:
        raise ValueError("Only yahoo_fin and alphavantage supported")
    ticker = namemap.get(ticker, ticker)
    try:

        if framework == 'yahoo_fin':
            df = si.get_data(ticker, start_date=start_date,end_date=end_date)
        elif framework == 'backtesting':
            df = bt.get(ticker, start=start_date, end=end_date)
        elif framework == 'alphavantage':
            key = API['alphavantage']
            ts = TimeSeries(key, output_format='pandas')
            df, metadata = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            df = df.loc[::-1].loc[start_date:end_date]
        elif framework == 'investpy':
            df = ipy.get_stock_historical_data(stock=ticker,
                                               country=country,
                                               from_date=start_date,
                                               to_date=end_date)
    except:
        df = None
    return df

