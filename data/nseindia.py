import requests
import json
import os
import argparse
import pandas as pd
import pickle as pkl
from typing import List

all_nse_urls = dict()
all_nse_urls['nifty_oc'] = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
all_nse_urls['banknifty_oc'] = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

def get_available_urls()->List:
    return list(all_nse_urls.values())

def get_url_keys()->List:
    return list(all_nse_urls.keys())

def get_url_from_key(key:str)->str:
    return all_nse_urls[key]

def get_nse_site_header():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    return headers

def get_data_from_nse(url: str, headers:str, use_cookies:bool=False):
    if use_cookies:
        print("yes for cookies")
        cookies = {'bm_sv':'_ga=GA1.2.360247993.1609388167; _gid=GA1.2.372894070.1618131763; nseQuoteSymbols=[{"symbol":"NIFTY","identifier":"OPTIDXNIFTY15-04-2021CE15000.00","type":"equity"}]; nsit=AwvZTBeZIh7Mbr9aIUALF3MH; AKA_A2=A; _gat_UA-143761337-1=1; ak_bmsc=541E4D6E5FA8E97D6867B856A83F788A170F2133DA0B0000B7FB7260E5032F1C~plEQkckmk6KEEPk5r/NUu/Svbgl3Goi+Wogm/MqN4u+bwHh/e0y/FH4vQ+jH3WyPosNJ+iUISukAfKjSv7Y5d1XX1N0VW0pamDQxTcgzmOtb6Ka8A68MSFHJf0BmG23ubrijEnrlPBzYtU6ZlzUZc0dhTYlsYDgU3EsNwWIkIhpG5Xzoe+5lSTMUPZDEeYBYtubIXxZPQXWUus/KMxoMiux8MjyKhe5SVAryi0W+cjCFTIn/jDaivX15LSxjPEIt+H; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTYxODE0ODMwMywiZXhwIjoxNjE4MTUxOTAzfQ.dAWGeib_QbQNcFAYD2kS206N8kKg7KCttlp6kgPF6kY; RT="sl=1&ss=knd7pfra&tt=135&bcn=//684fc53e.akstat.io/&z=1&dm=nseindia.com&si=8658f627-8fb6-468a-be69-4a85fe83e6b5&ld=k8d&nu=438a81dc254782a582cbf8bc8a031b93&cl=sca"; bm_sv=C2D99E013EF4B50EBC5603BF89857C6A~/u3vsyyi0zaFiA5qZDNEOdHuqf/PtFVMDA7TlTlMt22Z0W7GHzH1T6Gb874bERScU5mZmKdqQootcoDruCPvM/amNzhMsbZId7Og45Wv+mdoX7UBUgQNIBf2+utY4Ac/s66KnaQdO+r6xe1bo9cMQTJJ93UPTQJ7H+4VLPx3K+g='}
        session = requests.Session()
        for key, value in cookies.items():
            session.cookies.set(key, value)
        content = session.get(url, headers = headers)
    else:
        content = requests.get(url, headers = headers)
    if content.status_code==200:
        data = json.loads(content.text)
        return data
    else:
        print("Didn't get the response from NSE website")
        return None
def extract_underlying_data(data):
    index = data['records']['index']
    return pd.Series(index)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cookies', action='store_const', dest='use_cookies', default=False, const=True)
    parser.add_argument('data_type', help='What data to get option chain, live market -- [oc, price]')
    parser.add_argument('ticker', help='Ticker name')
    parser.add_argument('--nosave', action='store_const', dest='nosave', default=False, const=True)

    args = parser.parse_args()

    url_key = args.ticker+'_'+args.data_type
    url = all_nse_urls[url_key]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    data = get_data_from_nse(url, headers, use_cookies=args.use_cookies)
    if data is not None:
        print(data.keys())
        if not args.nosave:
            os.makedirs('./temp_files', exist_ok= True)
            with open("./temp_files/data.pkl", 'wb') as f:
                pkl.dump(data, f)
        if args.data_type == 'oc':
            print(data['records']['data'][0])
            pe_oc = pd.DataFrame()
            ce_oc = pd.DataFrame()

            for row in data['records']['data']:
                if 'PE' in row:
                    temp = pd.DataFrame(row['PE'])
                    pe_oc = pe_oc.append(temp)
                else:
                    temp = pd.DataFrame(row['CE'])
                    ce_oc = ce_oc.append(temp)

            #oc_df = pd.DataFrame(data['records'])
            #oc_filtered_df = pd.DataFrame(data['filtered'])


        #print(oc_df.shape)
        #print(oc_df.head(5))
