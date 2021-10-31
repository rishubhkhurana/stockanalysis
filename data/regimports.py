import numpy as np
import pandas as pd
import yahoo_fin as yf
import yahoo_fin.stock_info as si
import mplfinance as mpf
from yahoo_fin import options
import streamlit as st
#import bt
import investpy as ipy
import requests
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from argparse import ArgumentParser