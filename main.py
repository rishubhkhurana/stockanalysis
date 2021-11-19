import yaml
from data.datadownloader import *



if __name__ == '__main__':
    config_file = 'config.yml'
    # reading config file
    config = yaml.load(open(config_file), yaml.FullLoader)

    # getting data arguments
    ticker = config['data']['ticker']
    start = config['data']['start']
    end = config['data']['end']
    country = config['data']['country']
    framework = config['data']['framework']
    typ = config['data']['typ']
    # printing the log
    print("Config options for data:")
    print(f"Asset type: {typ}")
    print(f"Ticker: {ticker}")
    print(f'framework: {framework}')
    print(f"start date: {start}")
    print(f"end date: {end}")
    print(f'country: {country}')


    df = get_daily_historical_data(ticker,
                                   framework=framework,
                                   country=country,
                                   start_date=start,
                                   end_date=end,
                                   )

    print(f"Number of data points: {df.shape}")
    print(f"Peek into the data")
    print(df.head())
